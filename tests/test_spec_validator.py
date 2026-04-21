from __future__ import annotations

import unittest

from planning_agent.spec_validator import render_validation_markdown


SAMPLE_REPORT = {
    "title": "기획서 기준 기능 적합도 검증 리포트",
    "overall_score": 78,
    "verdict": "중간",
    "summary": "핵심 구조는 대체로 충족하지만 일부 운영 항목과 워크플로우 세부 구현이 부족합니다.",
    "section_scores": [
        {
            "section": "Work Process",
            "score": 82,
            "status": "양호",
            "summary": "AS-IS/TO-BE 구조가 대부분 반영됨",
            "evidence": ["CLI 호출 흐름 존재"],
            "gaps": ["실시간 모니터링 미흡"],
        }
    ],
    "requirement_checks": [
        {
            "requirement": "서브에이전트 위임 지원",
            "satisfied": True,
            "confidence": 0.9,
            "evidence": ["task 위임 흐름 존재"],
            "notes": "핵심 기능 확인",
        }
    ],
    "major_risks": ["운영 링크 미정"],
    "recommended_actions": ["TO-BE 단계별 세부 구현 보강"],
}


class SpecValidatorTests(unittest.TestCase):
    def test_render_validation_markdown_contains_key_sections(self) -> None:
        markdown = render_validation_markdown(SAMPLE_REPORT, "plan.md", "src")

        self.assertIn("# 기획서 기준 기능 적합도 검증 리포트", markdown)
        self.assertIn("## 섹션별 평가", markdown)
        self.assertIn("## 주요 요구사항 체크", markdown)
        self.assertIn("## 주요 리스크", markdown)
        self.assertIn("## 권장 조치", markdown)
        self.assertIn("| Work Process | 82 | 양호 |", markdown)
        self.assertIn("| 서브에이전트 위임 지원 | O | 0.9 |", markdown)


if __name__ == "__main__":
    unittest.main()
