from __future__ import annotations

import unittest
from pathlib import Path

from planning_agent.comparator import compare_sources, render_comparison_markdown


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class ComparatorTests(unittest.TestCase):
    def test_similar_repositories_score_higher_than_different_ones(self) -> None:
        similar = compare_sources(
            str(FIXTURES_DIR / "compare_repo_a"),
            str(FIXTURES_DIR / "compare_repo_b"),
        )
        different = compare_sources(
            str(FIXTURES_DIR / "compare_repo_a"),
            str(FIXTURES_DIR / "compare_repo_c"),
        )

        self.assertGreater(similar.overall_score, different.overall_score)
        self.assertEqual(similar.verdict, "높음")

    def test_render_comparison_markdown_contains_key_sections(self) -> None:
        result = compare_sources(
            str(FIXTURES_DIR / "compare_repo_a"),
            str(FIXTURES_DIR / "compare_repo_b"),
        )
        markdown = render_comparison_markdown(
            result,
            str(FIXTURES_DIR / "compare_repo_a"),
            str(FIXTURES_DIR / "compare_repo_b"),
        )

        self.assertIn("# 코드 기능 유사도 비교 리포트", markdown)
        self.assertIn("## 세부 지표", markdown)
        self.assertIn("## 주요 공통점/차이", markdown)
        self.assertIn("## 해석 가이드", markdown)


if __name__ == "__main__":
    unittest.main()
