from __future__ import annotations

import unittest
from pathlib import Path

from planning_agent.analyzer import summarize_codebase


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class AnalyzerTests(unittest.TestCase):
    def test_summarize_directory_skips_ignored_dirs(self) -> None:
        root = FIXTURES_DIR / "sample_repo"

        summary = summarize_codebase(str(root))

        self.assertEqual(summary.project_name, root.name)
        self.assertEqual(summary.file_count, 2)
        self.assertIn("### 파일: app.py", summary.summary_text)
        self.assertIn("### 파일: README.md", summary.summary_text)
        self.assertNotIn("ignored.js", summary.summary_text)

    def test_summarize_single_file(self) -> None:
        file_path = FIXTURES_DIR / "single_file.py"

        summary = summarize_codebase(str(file_path))

        self.assertEqual(summary.project_name, "single_file.py")
        self.assertEqual(summary.file_count, 1)
        self.assertIn("### 파일: single_file.py", summary.summary_text)
        self.assertIn("print(x)", summary.summary_text)

    def test_summarize_truncates_large_file_content(self) -> None:
        file_path = FIXTURES_DIR / "large_file.py"

        summary = summarize_codebase(str(file_path), max_chars_per_file=10)

        self.assertTrue(summary.summary_text.endswith("AAAAAAAAAA"))
        self.assertNotIn("AAAAAAAAAAA", summary.summary_text)


if __name__ == "__main__":
    unittest.main()
