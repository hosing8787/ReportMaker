from __future__ import annotations

import unittest

from planning_agent.render import render_markdown


SAMPLE_DOCUMENT = {
    "title": "테스트 문서",
    "background": ["코드 기반 자동 문서화 검증"],
    "purpose": ["샘플 양식과 유사한 출력 확인"],
    "writing_notes": ["링크는 확인 필요로 표기 가능"],
    "toc": ["개요", "Agent 유형 분류", "업무 Flow"],
    "overview": [{"label": "Agent 개요", "value": "설명|줄바꿈\n포함"}],
    "classification": [
        {
            "category": "행동 방식",
            "options": [
                {"label": "계획형", "checked": True, "note": "todo 기반"},
                {"label": "확장형", "checked": True, "note": "tool 사용"},
                {"label": "학습형", "checked": True, "note": "memory"},
            ],
        },
        {
            "category": "협력 방식",
            "options": [
                {"label": "협력 수행", "checked": True, "note": "sub-agent"},
            ],
        },
    ],
    "work_process": {
        "sample_flow_document": "샘플 문서.pptx",
        "sharepoint_link": "확인 필요",
        "file_naming": ["Rule : BA_XXX_Agent명.pptx"],
        "as_is": {
            "title": "현재 운영 흐름",
            "actors": ["운영자"],
            "steps": ["수동 점검", "수동 공유"],
            "outputs": ["Slack", "Email"],
        },
        "to_be": {
            "title": "목표 자동화 흐름",
            "actors": ["운영자", "Agent"],
            "steps": ["요청 입력", "자동 수집", "결과 공유"],
            "outputs": ["Slack Canvas"],
        },
        "implementation_architecture": [
            {"name": "Core Agent", "roles": ["입력 해석", "작업 분배"]},
            {"name": "Metric Agent", "roles": ["메트릭 수집", "결과 업데이트"]},
        ],
        "implementation_steps": [
            {"stage": "1단계 - 요청 입력", "details": ["Slack 요청 접수"]},
            {"stage": "2단계 - 결과 확인", "details": ["Slack Canvas 확인"]},
        ],
    },
    "tools": [
        {"category": "Message", "system": "Slack", "used": True, "purpose": "알림"},
        {"category": "KM", "system": "Confluence", "used": True, "purpose": "문서화"},
        {"category": "Cloud", "system": "Datadog", "used": True, "purpose": "모니터링"},
    ],
    "parameters": [{"system": "Azure", "name": "AZURE_OPENAI_ENDPOINT", "value": "엔드포인트"}],
    "considerations": ["민감정보 주의"],
    "assumptions": ["사내 환경 실행"],
}


class RenderTests(unittest.TestCase):
    def test_render_markdown_contains_expected_sections(self) -> None:
        markdown = render_markdown(SAMPLE_DOCUMENT)

        self.assertIn("# 테스트 문서", markdown)
        self.assertIn("- 작성 배경", markdown)
        self.assertIn("## 문서 목차", markdown)
        self.assertIn("## 1. 개요 (Overview)", markdown)
        self.assertIn("## 6. 기타 참고사항 및 제약조건", markdown)
        self.assertIn("설명\\|줄바꿈<br>포함", markdown)
        self.assertIn("| 구분 | 유형 |", markdown)
        self.assertIn("| 행동 방식 | [ ] 자율형 (Autonomy) : 외부의 지시 없이 스스로 동작 (Event 발생 시 수행 등) |", markdown)
        self.assertIn("|  | [x] 계획형 (Planning) : 정해진 스케줄에 따라 동작 (Daily, Monthly 등) |", markdown)
        self.assertIn("|  | [x] 확장형 (Tool Use) : 외부 Tool 활용 |", markdown)
        self.assertIn("|  | [x] 학습형 (Memory) : 데이터 수집 및 VectorDB 저장, Report 작성 |", markdown)
        self.assertIn("| 협력 방식 | [ ] 단독 수행 (Single) : Agent 혼자 동작 |", markdown)
        self.assertIn("|  | [x] 협력 수행 (Multi) : Agent 간 호출 및 결과 활용 (A -> B 호출) |", markdown)
        self.assertIn("- 샘플 Flow 문서 : 샘플 문서.pptx", markdown)
        self.assertIn("| 업무 Flow (AS-IS) |", markdown)
        self.assertIn("흐름: 수동 점검 -> 수동 공유", markdown)
        self.assertIn("| 구현 단계 | 내용 |", markdown)
        self.assertIn("| 1단계 - 요청 입력 | Slack 요청 접수 |", markdown)
        self.assertIn("## 4. 운영 Tool 리스트 (Tool List)", markdown)
        self.assertIn("| 구분 | 관리 시스템 | 사내 시스템 | 고객사 시스템 | Message | KM | ... |", markdown)
        self.assertIn("[x] Slack", markdown)
        self.assertIn("[x] Confluence", markdown)
        self.assertIn("| 구분 | Log | Cloud | 서버(OS) | DB | MW | Kubernetes | Network | AI DC |", markdown)
        self.assertIn("[x] Datadog", markdown)
        self.assertIn("- 민감정보 주의", markdown)
        self.assertIn("- 사내 환경 실행", markdown)

    def test_render_markdown_fills_empty_lists(self) -> None:
        empty_document = {
            **SAMPLE_DOCUMENT,
            "background": [],
            "purpose": [],
            "writing_notes": [],
            "toc": [],
            "considerations": [],
            "assumptions": [],
            "work_process": {
                "sample_flow_document": "",
                "sharepoint_link": "",
                "file_naming": [],
                "as_is": {"title": "", "actors": [], "steps": [], "outputs": []},
                "to_be": {"title": "", "actors": [], "steps": [], "outputs": []},
                "implementation_architecture": [],
                "implementation_steps": [],
            },
            "tools": [],
            "parameters": [],
        }

        markdown = render_markdown(empty_document)

        self.assertIn("- 확인 필요", markdown)
        self.assertIn("- 없음", markdown)
        self.assertIn("| 업무 Flow (AS-IS) | 확인 필요 |", markdown)
        self.assertIn("| 확인 필요 | 확인 필요 |", markdown)
        self.assertIn("[ ] Work Portal", markdown)
        self.assertIn("[ ] Slack", markdown)
        self.assertIn("[ ] Datadog", markdown)
        self.assertIn("| 확인 필요 | 확인 필요 | 확인 필요 |", markdown)


if __name__ == "__main__":
    unittest.main()
