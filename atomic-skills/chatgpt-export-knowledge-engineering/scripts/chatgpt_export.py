#!/usr/bin/env python3
"""Local-first, dependency-free ChatGPT export inventory and text normalization.

The exporter is an evolving product format, not a public fixed JSON schema.
This utility never extracts ZIP members or sends data over a network.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import heapq
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

MAX_ENTRIES = 100_000
MAX_MEMBER = 512 * 1024 * 1024
MAX_TOTAL_JSON = 1024 * 1024 * 1024
MAX_RATIO = 1000
CONVERSATIONS_JSON = re.compile(r"^conversations?(?:[-_]?\d+)?\.json$", re.I)
ASSET_KEYS = {"asset_pointer", "file_id", "asset_id", "file_name", "filename"}


def is_conversations_json(name: str) -> bool:
    return bool(CONVERSATIONS_JSON.fullmatch(PurePosixPath(name).name))


def safe_zip_info(info: zipfile.ZipInfo) -> None:
    name = info.filename
    path = PurePosixPath(name)
    if (not name or "\\" in name or path.is_absolute() or ".." in path.parts
            or ":" in path.parts[0] or "\x00" in name):
        raise ValueError("Unsafe ZIP entry path")
    if stat.S_ISLNK(info.external_attr >> 16):
        raise ValueError("ZIP contains a symbolic link")
    if info.file_size > MAX_MEMBER:
        raise ValueError("ZIP member exceeds size limit")
    if info.file_size and info.file_size / max(info.compress_size, 1) > MAX_RATIO:
        raise ValueError("Excessive ZIP compression ratio")


def load_sources(source: Path):
    """Yield (member_name, parsed JSON, raw_sha256); return asset inventory."""
    if source.is_file() and zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            infos = archive.infolist()
            if len(infos) > MAX_ENTRIES:
                raise ValueError("Too many ZIP entries")
            seen = set()
            total_json = 0
            for info in infos:
                safe_zip_info(info)
                if info.filename in seen:
                    raise ValueError("Duplicate ZIP entry names")
                seen.add(info.filename)
                if not info.is_dir() and is_conversations_json(info.filename):
                    total_json += info.file_size
                    if total_json > MAX_TOTAL_JSON:
                        raise ValueError("Conversation JSON exceeds aggregate size limit")
                    raw = archive.read(info)
                    if len(raw) > MAX_MEMBER:
                        raise ValueError("Member exceeds uncompressed read limit")
                    yield info.filename, json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()
    elif source.is_dir():
        root = source.resolve(strict=True)
        paths = sorted(source.rglob("*"))
        if len(paths) > MAX_ENTRIES:
            raise ValueError("Too many source files")
        total_json = 0
        for path in paths:
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("Symlink or escaped file in input tree")
            if path.is_file() and is_conversations_json(path.name):
                size = path.stat().st_size
                total_json += size
                if size > MAX_MEMBER or total_json > MAX_TOTAL_JSON:
                    raise ValueError("Conversation JSON exceeds size limit")
                raw = path.read_bytes()
                yield path.relative_to(source).as_posix(), json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()
    else:
        raise ValueError("Input must be an export ZIP or extracted directory")


def iter_conversations(document):
    if isinstance(document, list):
        records = document
    elif isinstance(document, dict) and isinstance(document.get("conversations"), list):
        records = document["conversations"]
    else:
        raise ValueError("Unrecognized conversation JSON top-level format")
    for record in records:
        if isinstance(record, dict):
            yield record


def as_iso(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError, OSError):
        return None


def extract_content(content):
    """Return visible text, non-text part count and opaque asset references."""
    if not isinstance(content, dict):
        return "", 1, []
    pieces = []
    unsupported = 0
    asset_refs = []
    parts = content.get("parts")
    if not isinstance(parts, list):
        parts = [content.get("text")] if "text" in content else []
        if not parts and content.get("content_type") not in (None, "text"):
            unsupported += 1
    for part in parts:
        if isinstance(part, str):
            pieces.append(part)
        elif isinstance(part, dict):
            if isinstance(part.get("text"), str):
                pieces.append(part["text"])
            else:
                unsupported += 1
            for key in ASSET_KEYS:
                ref = part.get(key)
                if isinstance(ref, str) and ref:
                    asset_refs.append({"key": key, "value": ref[:1000]})
        elif part is not None:
            unsupported += 1
    for key in ASSET_KEYS:
        ref = content.get(key)
        if isinstance(ref, str) and ref:
            asset_refs.append({"key": key, "value": ref[:1000]})
    return "\n".join(pieces), unsupported, asset_refs


def node_order(mapping, current_node, mode, warnings):
    if mode == "current" and current_node in mapping:
        seen, route = set(), []
        node_id = current_node
        while node_id is not None:
            if node_id in seen:
                warnings.append("Cycle detected in active path; stopped traversal")
                break
            seen.add(node_id)
            node = mapping.get(node_id)
            if not isinstance(node, dict):
                warnings.append("Dangling parent in active path")
                break
            route.append(node_id)
            node_id = node.get("parent")
        return list(reversed(route)), "current"
    if mode == "current":
        warnings.append("Missing current_node; preserved all nodes rather than guessing branch")
    # Kahn ordering: parent before child; UTC timestamps are tie-breakers only.
    degree = {key: 0 for key in mapping}
    children = defaultdict(list)
    for key, node in mapping.items():
        if not isinstance(node, dict):
            continue
        parent = node.get("parent")
        if parent in mapping:
            children[parent].append(key)
            degree[key] += 1
        elif parent is not None:
            warnings.append("Dangling parent in mapping")
    def priority(key):
        node = mapping.get(key)
        message = node.get("message") if isinstance(node, dict) else None
        message = message if isinstance(message, dict) else {}
        return (message.get("create_time") if isinstance(message.get("create_time"), (int, float)) else 0, str(key))
    heap = [(priority(key), key) for key, value in degree.items() if value == 0]
    heapq.heapify(heap)
    result = []
    while heap:
        _, key = heapq.heappop(heap)
        result.append(key)
        for child in children[key]:
            degree[child] -= 1
            if degree[child] == 0:
                heapq.heappush(heap, (priority(child), child))
    if len(result) != len(mapping):
        warnings.append("Cycle or malformed graph: remaining nodes appended deterministically")
        result.extend(sorted((k for k in mapping if k not in set(result)), key=str))
    return result, "all"


def normalize_conversation(conversation, mode):
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return [], ["Missing or invalid mapping"], "none"
    warnings = []
    keys, effective_mode = node_order(mapping, conversation.get("current_node"), mode, warnings)
    records = []
    for node_id in keys:
        node = mapping.get(node_id)
        if not isinstance(node, dict) or not isinstance(node.get("message"), dict):
            continue
        message = node["message"]
        author = message.get("author") if isinstance(message.get("author"), dict) else {}
        content = message.get("content")
        text, unsupported, refs = extract_content(content)
        records.append({
            "conversation_id": conversation["id"],
            "source_member": conversation.get("_node_sources", {}).get(node_id, {}).get("member"),
            "source_json_sha256": conversation.get("_node_sources", {}).get(node_id, {}).get("sha256"),
            "node_id": node_id,
            "parent_node_id": node.get("parent"),
            "message_id": message.get("id"),
            "role": author.get("role"),
            "author_name": author.get("name"),
            "recipient": message.get("recipient"),
            "channel": (message.get("metadata") or {}).get("channel") if isinstance(message.get("metadata"), dict) else None,
            "created_at": as_iso(message.get("create_time")),
            "content_type": content.get("content_type") if isinstance(content, dict) else None,
            "text": text,
            "nontext_parts": unsupported,
            "asset_refs": refs,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "branch_mode": effective_mode,
        })
    return records, warnings, effective_mode


def safe_md_text(text):
    # Code fences prevent active Markdown links, images and embedded HTML.
    longest = max((len(match.group()) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def run(source, out, mode):
    merged = {}
    json_files = []
    conflicts = []
    for name, doc, digest in load_sources(source):
        json_files.append({"member": name, "sha256": digest})
        for index, raw in enumerate(iter_conversations(doc)):
            cid = str(raw.get("id") or raw.get("conversation_id") or f"unknown:{name}:{index}")
            raw = dict(raw, id=cid)
            if cid not in merged:
                merged[cid] = dict(raw, _sources=[name], _node_sources={
                    key: {"member": name, "sha256": digest}
                    for key in (raw.get("mapping") or {})
                })
                continue
            existing = merged[cid]
            existing["_sources"].append(name)
            other_nodes = raw.get("mapping")
            if isinstance(other_nodes, dict) and isinstance(existing.get("mapping"), dict):
                for node_id, node in other_nodes.items():
                    if node_id in existing["mapping"] and existing["mapping"][node_id] != node:
                        conflicts.append({"conversation_id": cid, "node_id": node_id, "source": name})
                    elif node_id not in existing["mapping"]:
                        existing["mapping"][node_id] = node
                        existing["_node_sources"][node_id] = {"member": name, "sha256": digest}
            for key in ("title", "create_time", "update_time", "current_node"):
                if existing.get(key) is None and raw.get(key) is not None:
                    existing[key] = raw[key]
    if conflicts:
        raise ValueError(f"Conflicting duplicate nodes ({len(conflicts)}); refusing silent overwrite")
    if not json_files:
        raise ValueError("No conversations JSON files recognized in export")
    os.umask(0o077)
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    chats_dir = out / "chats"
    chats_dir.mkdir(exist_ok=True, mode=0o700)
    conv_rows, message_rows, warnings = [], [], []
    for i, cid in enumerate(sorted(merged)):
        conversation = merged[cid]
        messages, errors, effective = normalize_conversation(conversation, mode)
        message_rows.extend(messages)
        title = str(conversation.get("title") or "Untitled")
        slug = re.sub(r"[^\w-]+", "-", title, flags=re.U).strip("-_")[:60] or "chat"
        md_name = f"{i:05d}-{slug}-{hashlib.sha256(cid.encode()).hexdigest()[:10]}.md"
        lines = [f"# {html.escape(title, quote=False)}", "", f"Conversation ID: {html.escape(cid)}", f"Branch: {effective}", ""]
        for msg in messages:
            who = msg["role"] or "unknown"
            lines.extend([f"## {html.escape(str(who))} · {html.escape(str(msg['node_id']))}", "", safe_md_text(msg["text"]), ""])
            if msg["nontext_parts"]:
                lines.extend([f"[Non-text parts not rendered: {msg['nontext_parts']}; see messages.jsonl and original ZIP]", ""])
        (chats_dir / md_name).write_text("\n".join(lines), encoding="utf-8")
        conv_rows.append({
            "conversation_id": cid,
            "title": title,
            "created_at": as_iso(conversation.get("create_time")),
            "updated_at": as_iso(conversation.get("update_time")),
            "current_node": conversation.get("current_node"),
            "source_members": sorted(set(conversation["_sources"])),
            "message_count": len(messages),
            "branch_mode": effective,
            "markdown": f"chats/{md_name}",
            "warnings": errors,
        })
        warnings.extend({"conversation_id": cid, "issue": error} for error in errors)
    write_jsonl(out / "conversations.jsonl", conv_rows)
    write_jsonl(out / "messages.jsonl", message_rows)
    manifest = {
        "format": "chatgpt-export-normalized-v1", "input": source.name,
        "source_json": json_files, "requested_mode": mode,
        "conversations": len(conv_rows), "messages": len(message_rows),
        "nontext_parts": sum(row["nontext_parts"] for row in message_rows),
        "warnings": warnings,
        "note": "Source is authoritative; Markdown/JSONL are lossy text views. Do not upload private exports to public repositories.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original ChatGPT export ZIP or extracted directory")
    parser.add_argument("--out", type=Path, default=Path("chatgpt-normalized"))
    parser.add_argument("--mode", choices=("current", "all"), default="current")
    args = parser.parse_args(argv)
    try:
        result = run(args.source, args.out, args.mode)
    except (ValueError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps({key: result[key] for key in ("conversations", "messages", "nontext_parts")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
