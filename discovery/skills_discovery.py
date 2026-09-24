#!/usr/bin/env python3
"""Local, dependency-free skill discovery: index, hybrid search, eval."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WORDS = re.compile(r"[^\W_]+", re.UNICODE)


def tok(text):
    return WORDS.findall(text.casefold().replace("-", " ").replace("_", " "))


def frontmatter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result = {}
    key = None
    parts = []
    block = False

    def flush():
        if key in ("name", "description"):
            result[key] = " ".join(p.strip() for p in parts if p.strip()).strip(" \"'")

    for line in lines[1:]:
        if line.strip() == "---":
            flush()
            return result
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            flush()
            key, value = match.groups()
            block = value in ("|", "|-", ">", ">-")
            parts = [] if block else [value.split(" #", 1)[0]]
        elif block and (line.startswith(" ") or not line.strip()):
            parts.append(line)
        elif not line.startswith(" "):
            flush()
            key, parts, block = None, [], False
    return result


def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def read_index(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()] if path.exists() else []


def build(root, index, check=False):
    directory = root / "skills"
    if not directory.is_dir():
        raise ValueError("Missing skills/ directory")
    overrides = read_json(root / "discovery" / "overrides.json", {})
    previous = {x["path"]: x for x in read_index(index)}
    rows, reused = [], 0
    for file in sorted(directory.rglob("SKILL.md")):
        if file.is_symlink() or not file.is_file():
            continue
        try:
            file.resolve().relative_to(directory.resolve())
        except ValueError:
            continue
        path = file.relative_to(root).as_posix()
        data = file.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        extra = overrides.get(file.parent.name, {})
        old = previous.get(path)
        if old and old.get("sha256") == digest and old.get("overrides") == extra:
            rows.append(old)
            reused += 1
            continue
        meta = frontmatter(data.decode("utf-8", "replace"))
        rows.append(dict(name=meta.get("name") or file.parent.name,
                         description=meta.get("description") or "",
                         path=path, sha256=digest, overrides=extra,
                         aliases=extra.get("aliases", []),
                         negative_intents=extra.get("negative_intents", []),
                         domain=extra.get("domain", ""),
                         requires=extra.get("requires", []),
                         support=extra.get("support", []),
                         check=extra.get("check", []),
                         avoid=extra.get("avoid", [])))
    content = "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n"
                      for x in sorted(rows, key=lambda row: row["path"]))
    if check:
        return len(rows), reused, index.exists() and index.read_text(encoding="utf-8") == content
    if not index.exists() or index.read_text(encoding="utf-8") != content:
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(content, encoding="utf-8")
    return len(rows), reused, True


def grams(value):
    value = " " + " ".join(tok(value)) + " "
    return Counter(value[i:i + 3] for i in range(len(value) - 2))


def search(query, rows, top_k=5, min_score=0.22):
    """Field-weighted BM25 plus character-trigram TF-IDF cosine (not embeddings)."""
    qt = tok(query)
    if not qt or top_k < 1:
        return []
    docs, df, gdf = [], Counter(), Counter()
    qgrams = grams(query)
    for row in rows:
        title = row["name"]
        alias = " ".join(row.get("aliases", []))
        desc = row.get("description", "")[:1000]
        terms = tok(title) * 4 + tok(alias) * 5 + tok(desc) * 2 + tok(row.get("domain", ""))
        counts = Counter(terms)
        cgrams = grams(" ".join((title, alias, desc[:400])))
        df.update(counts.keys())
        gdf.update(cgrams.keys())
        docs.append((row, counts, cgrams, max(1, len(terms))))
    n = len(docs)
    if not n:
        return []
    avg = sum(x[3] for x in docs) / n
    idf = {g: math.log(1 + (n - gdf[g] + .5) / (gdf[g] + .5)) for g in qgrams}
    qnorm = math.sqrt(sum((v * idf[g]) ** 2 for g, v in qgrams.items()))
    output = []
    lowered = query.casefold()
    for row, counts, cgrams, length in docs:
        if any(x and x.casefold() in lowered for x in row.get("negative_intents", [])):
            continue
        bm = sum(math.log(1 + (n - df[t] + .5) / (df[t] + .5)) * counts[t] * 2.2
                 / (counts[t] + 1.2 * (.25 + .75 * length / avg))
                 for t in set(qt) if counts[t]) / len(set(qt))
        dot = sum(v * idf[g] ** 2 * cgrams.get(g, 0) for g, v in qgrams.items())
        dnorm = math.sqrt(sum((cgrams.get(g, 0) * idf[g]) ** 2 for g in qgrams))
        fuzzy = dot / (qnorm * dnorm) if qnorm and dnorm else 0.0
        needle = " ".join(qt)
        exact = 3.0 if needle == " ".join(tok(row["name"])) else (
            1.8 if needle in [" ".join(tok(a)) for a in row.get("aliases", [])] else 0.0)
        score = .8 * bm + .7 * fuzzy + exact
        if score >= min_score:
            output.append(dict(name=row["name"], path=row["path"],
                               description=row.get("description", ""),
                               score=round(score, 5),
                               signals=dict(bm25=round(bm, 4), trigram=round(fuzzy, 4), exact=exact),
                               requires=row.get("requires", []),
                               support=row.get("support", []),
                               check=row.get("check", []),
                               avoid=row.get("avoid", [])))
    return sorted(output, key=lambda x: (-x["score"], x["path"]))[:top_k]


def evaluate(rows, dataset):
    cases = read_index(dataset)
    if not cases:
        raise ValueError("Empty evaluation dataset")
    positives = no_skill = hits1 = hits5 = no_hits = 0
    mrr = 0
    misses = []
    for case in cases:
        found = search(case["query"], rows, 5, case.get("min_score", .22))
        expected = case.get("expected", [])
        if not expected:
            no_skill += 1
            no_hits += not found
            if found:
                misses.append(dict(query=case["query"], found=[x["path"] for x in found]))
            continue
        positives += 1
        rank = next((i + 1 for i, x in enumerate(found)
                     if x["path"] in expected or Path(x["path"]).parent.name in expected), None)
        if rank:
            hits1 += rank == 1
            hits5 += rank <= 5
            mrr += 1 / rank
        else:
            misses.append(dict(query=case["query"], expected=expected,
                               found=[x["path"] for x in found]))
    return dict(cases=len(cases), positive_cases=positives, no_skill_cases=no_skill,
                recall_at_1=round(hits1 / positives, 4) if positives else None,
                recall_at_5=round(hits5 / positives, 4) if positives else None,
                mrr_at_5=round(mrr / positives, 4) if positives else None,
                no_skill_accuracy=round(no_hits / no_skill, 4) if no_skill else None,
                misses=misses,
                note="Routing metrics only; token savings and downstream quality not measured.")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=ROOT)
    cli.add_argument("--index", type=Path)
    commands = cli.add_subparsers(dest="cmd", required=True)
    idx = commands.add_parser("index")
    idx.add_argument("--check", action="store_true")
    srch = commands.add_parser("search")
    srch.add_argument("query")
    srch.add_argument("--top-k", type=int, default=5)
    srch.add_argument("--min-score", type=float, default=.22)
    ev = commands.add_parser("eval")
    ev.add_argument("--dataset", type=Path)
    args = cli.parse_args()
    root = args.root.resolve()
    path = args.index or root / "skills-index.jsonl"
    if args.cmd == "index":
        count, reused, ok = build(root, path, args.check)
        print(json.dumps(dict(skills=count, reused=reused, check_passed=ok)))
        return 0 if ok else 1
    rows = read_index(path)
    if not rows:
        print("Missing index: run python discovery/skills_discovery.py index", file=sys.stderr)
        return 2
    if args.cmd == "search":
        print(json.dumps(dict(query=args.query, results=search(args.query, rows,
              args.top_k, args.min_score)), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(evaluate(rows, args.dataset or root / "discovery" / "eval.jsonl"),
                         ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
