"""Synthetic offline regression tests; no personal data."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile

from chatgpt_export import run, extract_content, node_order


def sample():
    return [{
        "id": "chat-1", "title": "Исследование / тест", "create_time": 1700000000,
        "current_node": "a3", "mapping": {
            "root": {"parent": None, "children": ["a1"], "message": None},
            "a1": {"parent": "root", "children": ["a2", "a2b"], "message": {
                "id": "msg1", "author": {"role": "user"}, "create_time": 1700000001,
                "content": {"content_type": "text", "parts": ["Hello"]}}},
            "a2": {"parent": "a1", "children": ["a3"], "message": {
                "id": "msg2", "author": {"role": "assistant"}, "create_time": 1700000002,
                "content": {"content_type": "text", "parts": ["old reply"]}}},
            "a2b": {"parent": "a1", "children": [], "message": {
                "id": "msg2b", "author": {"role": "assistant"}, "create_time": 1700000002,
                "content": {"content_type": "text", "parts": ["other branch"]}}},
            "a3": {"parent": "a2", "children": [], "message": {
                "id": "msg3", "author": {"role": "tool", "name": "python"},
                "content": {"content_type": "multimodal", "parts": ["42", {"asset_pointer": "asset-1"}]}}},
        }}]


class TestExport(unittest.TestCase):
    def test_active_branch_vs_all(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(root / "in.zip", "w") as z:
                z.writestr("conversations.json", json.dumps(sample()))
            current = run(root / "in.zip", root / "out1", "current")
            all_nodes = run(root / "in.zip", root / "out2", "all")
            self.assertEqual(current["messages"], 3)
            self.assertEqual(all_nodes["messages"], 4)
            rows = [json.loads(x) for x in (root / "out1/messages.jsonl").read_text().splitlines()]
            self.assertEqual([x["node_id"] for x in rows], ["a1", "a2", "a3"])
            self.assertEqual(rows[-1]["role"], "tool")
            self.assertEqual(rows[-1]["source_member"], "conversations.json")
            self.assertEqual(len(rows[-1]["source_json_sha256"]), 64)
            self.assertEqual(current["nontext_parts"], 1)
            self.assertNotIn("other branch", (root / "out1/messages.jsonl").read_text())

    def test_numbered_json_split_deduplicates(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(root / "in.zip", "w") as z:
                z.writestr("folder/conversations_1.json", json.dumps(sample()))
                z.writestr("folder/conversations-2.json", json.dumps(sample()))
            result = run(root / "in.zip", root / "out", "all")
            self.assertEqual(result["conversations"], 1)
            self.assertEqual(result["messages"], 4)

    def test_missing_current_node_preserves_all(self):
        conv = sample()[0]
        ids, effective = node_order(conv["mapping"], None, "current", [])
        self.assertEqual(effective, "all")
        self.assertEqual(len(ids), 5)
        self.assertLess(ids.index("a1"), ids.index("a2"))

    def test_nontext_is_explicit(self):
        text, count, refs = extract_content({"parts": ["text", {"asset_pointer": "X"}, {"text": "more"}, 9]})
        self.assertEqual(text, "text\nmore")
        self.assertEqual(count, 2)
        self.assertEqual(refs[0]["value"], "X")

    def test_zip_slip_rejected(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(root / "in.zip", "w") as z:
                z.writestr("../escape.txt", "bad")
                z.writestr("conversations.json", json.dumps(sample()))
            with self.assertRaisesRegex(ValueError, "Unsafe ZIP"):
                run(root / "in.zip", root / "out", "current")

    def test_conflicting_duplicate_nodes_fail(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            altered = sample()
            altered[0]["mapping"]["a1"]["message"]["content"]["parts"] = ["different"]
            with zipfile.ZipFile(root / "in.zip", "w") as z:
                z.writestr("conversations_1.json", json.dumps(sample()))
                z.writestr("conversations_2.json", json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "Conflicting duplicate"):
                run(root / "in.zip", root / "out", "all")


if __name__ == "__main__":
    unittest.main()
