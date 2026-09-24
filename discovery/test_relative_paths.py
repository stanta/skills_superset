"""Regression tests for path depth, traversal and real targets (CI only)."""
from pathlib import Path
import tempfile
import unittest
from validate_metaskills import ATOMIC, META, ROOT, resolve_atomic_reference


class RelativePathTests(unittest.TestCase):
    def test_meta_directory_and_catalog_directory_have_different_depths(self):
        meta = META / "meta-agent-systems" / "SKILL.md"
        child = META / "meta-agent-systems" / "references" / "members.md"
        target = ATOMIC / "agent-evals-lab" / "SKILL.md"
        self.assertEqual(resolve_atomic_reference(
            meta, "../../atomic-skills/agent-evals-lab/SKILL.md"), target.resolve())
        self.assertEqual(resolve_atomic_reference(
            child, "../../../atomic-skills/agent-evals-lab/SKILL.md"), target.resolve())

    def test_original_root_relative_reference_is_rejected_from_catalog(self):
        source = META / "meta-agent-systems" / "references" / "members.md"
        for wrong in ["atomic-skills/agent-evals-lab/SKILL.md",
                      "../../atomic-skills/agent-evals-lab/SKILL.md",
                      "../../../../atomic-skills/agent-evals-lab/SKILL.md"]:
            with self.subTest(wrong=wrong), self.assertRaises(AssertionError):
                resolve_atomic_reference(source, wrong)

    def test_original_root_relative_reference_is_rejected_from_meta(self):
        meta = META / "meta-agent-systems" / "SKILL.md"
        with self.assertRaises(AssertionError):
            resolve_atomic_reference(meta, "atomic-skills/agent-evals-lab/SKILL.md")
        with self.assertRaises(AssertionError):
            resolve_atomic_reference(meta, "../../../atomic-skills/agent-evals-lab/SKILL.md")

    def test_nested_atomic_skill_paths(self):
        source = META / "meta-office-documents" / "references" / "members.md"
        expected = ATOMIC / "build-report" / "report-to-pdf" / "SKILL.md"
        self.assertEqual(resolve_atomic_reference(
            source, "../../../atomic-skills/build-report/report-to-pdf/SKILL.md"),
            expected.resolve())

    def test_missing_or_traversal_target(self):
        source = META / "meta-agent-systems" / "references" / "members.md"
        for wrong in ["../../../atomic-skills/not-existent/SKILL.md",
                      "../../../atomic-skills/../README.md",
                      "../../../atomic-skills/agent-evals-lab/../README.md"]:
            with self.subTest(wrong=wrong), self.assertRaises(AssertionError):
                resolve_atomic_reference(source, wrong)


if __name__ == "__main__":
    unittest.main()
