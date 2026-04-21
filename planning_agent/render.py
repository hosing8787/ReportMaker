from __future__ import annotations


CLASSIFICATION_TEMPLATE = [
    (
        "행동 방식",
        [
            ("자율형 (Autonomy)", "외부의 지시 없이 스스로 동작 (Event 발생 시 수행 등)", ["autonomy", "자율"]),
            ("계획형 (Planning)", "정해진 스케줄에 따라 동작 (Daily, Monthly 등)", ["planning", "plan", "todo", "계획"]),
            ("확장형 (Tool Use)", "외부 Tool 활용", ["tool", "filesystem", "shell", "mcp", "protocol", "cli", "sdk", "확장"]),
            ("학습형 (Memory)", "데이터 수집 및 VectorDB 저장, Report 작성", ["memory", "context", "cache", "summary", "학습"]),
        ],
    ),
    (
        "목적",
        [
            ("단순 반사 (Simple)", "하나의 Event 발생 시 동작", ["simple", "single event", "단순"]),
            ("복합 반사 (Complex)", "두 개 이상의 Event 발생 시 동작", ["complex", "복합"]),
            ("수집/분석 (Memory)", "데이터 패턴 비교 및 이상 징후 감지 시 동작", ["analysis", "collect", "evaluate", "monitor", "수집", "분석"]),
            ("자가복구 (Self Healing)", "정의된 정상 상태가 아닐 경우 복구 동작 수행", ["self healing", "recover", "복구"]),
        ],
    ),
    (
        "협력 방식",
        [
            ("단독 수행 (Single)", "Agent 혼자 동작", ["single", "standalone", "단독"]),
            ("협력 수행 (Multi)", "Agent 간 호출 및 결과 활용 (A -> B 호출)", ["sub-agent", "subagent", "delegate", "multi", "worker", "협력"]),
        ],
    ),
]

TOOL_FIXED_LAYOUTS = [
    (
        "사내/고객사의 운영 관리 시스템",
        [
            ("관리 시스템", []),
            ("사내 시스템", ["Work Portal", "통풍감", "MCMP", "OPMATE", "ServiceFlow", "..."]),
            ("고객사 시스템", ["ServiceNow", "Jira", "Confluence", "..."]),
            ("Message", ["Slack", "Email", "SMS", "..."]),
            ("KM", ["AirTable", "Confluence", "Jira", "GitLab", "..."]),
            ("...", ["...", "..."]),
        ],
    ),
    (
        "Tower별 운영 솔루션",
        [
            ("Log", ["Splunk", "AMON", "통풍감", "..."]),
            ("Cloud", ["Datadog", "..."]),
            ("서버(OS)", ["AnyCatcher (On-Prem)", "Ontune (On-Prem)", "Ontune (k8s)", "..."]),
            ("DB", ["Prometheus", "Grafana", "Sherpa", "..."]),
            ("MW", ["Pinpoint", "EnPharos", "..."]),
            ("Kubernetes", ["Prometheus", "Grafana", "..."]),
            ("Network", ["NMS", "Telenet Center", "..."]),
            ("AI DC", ["DCIM", "..."]),
        ],
    ),
]


def _escape_cell(value: str) -> str:
    return value.replace("\n", "<br>").replace("|", "\\|").strip()


def _render_simple_bullets(title: str, items: list[str], empty_fallback: str = "확인 필요") -> str:
    lines = [f"- {title}"]
    if items:
        for item in items:
            lines.append(f"  - {item}")
    else:
        lines.append(f"  - {empty_fallback}")
    return "\n".join(lines)


def _render_overview(rows: list[dict]) -> str:
    lines = ["## 1. 개요 (Overview)", "", "| 항목 | 내용 |", "|---|---|"]
    for row in rows:
        lines.append(f"| {_escape_cell(row['label'])} | {_escape_cell(row['value'])} |")
    lines.append("")
    return "\n".join(lines)


def _render_classification(groups: list[dict], context_text: str) -> str:
    checked_text = f"{_collect_classification_text(groups)} {context_text}".strip()
    lines = ["## 2. Agent 유형 분류 (Classification)", "", "| 구분 | 유형 |", "|---|---|"]
    for category, options in CLASSIFICATION_TEMPLATE:
        for index, (label, note, keywords) in enumerate(options):
            mark = "[x]" if _matches_keywords(checked_text, keywords) else "[ ]"
            text = f"{mark} {label} : {note}"
            category_cell = _escape_cell(category) if index == 0 else ""
            lines.append(f"| {category_cell} | {_escape_cell(text)} |")
    lines.append("")
    return "\n".join(lines)


def _render_work_process(rows: dict) -> str:
    lines = ["## 3. 업무 Flow 변화 & 구현 방안 (Work Process)", ""]
    lines.append(f"- 샘플 Flow 문서 : {_escape_cell(rows['sample_flow_document']) or '확인 필요'}")
    lines.append(f"- Sharepoint 링크 : {_escape_cell(rows['sharepoint_link']) or '확인 필요'}")
    lines.append("- 파일 네이밍")
    if rows["file_naming"]:
        for item in rows["file_naming"]:
            lines.append(f"  - {item}")
    else:
        lines.append("  - 확인 필요")
    lines.append("")

    lines.append("| 구분 | 내용 |")
    lines.append("|---|---|")
    lines.append(f"| 업무 Flow (AS-IS) | {_render_flow_block(rows['as_is'])} |")
    lines.append(f"| 업무 Flow (TO-BE) | {_render_flow_block(rows['to_be'])} |")
    lines.append(f"| 구현 방안 | {_render_architecture(rows['implementation_architecture'])} |")
    lines.append("")

    lines.append("| 구현 단계 | 내용 |")
    lines.append("|---|---|")
    for item in rows["implementation_steps"]:
        details = "<br>".join(_escape_cell(detail) for detail in item["details"]) if item["details"] else "확인 필요"
        lines.append(f"| {_escape_cell(item['stage'])} | {details} |")
    if not rows["implementation_steps"]:
        lines.append("| 확인 필요 | 확인 필요 |")
    lines.append("")
    return "\n".join(lines)


def _render_tools(rows: list[dict], context_text: str) -> str:
    detected = f"{_collect_tool_text(rows)} {context_text}".strip()
    lines = ["## 4. 운영 Tool 리스트 (Tool List)", "", "- 추가가 필요한 경우 자유롭게 추가", ""]

    for section_name, columns in TOOL_FIXED_LAYOUTS:
        header_titles = [column for column, _ in columns]
        lines.append("| 구분 | " + " | ".join(header_titles) + " |")
        lines.append("|" + "---|" * (len(header_titles) + 1))
        cells: list[str] = []
        for _, options in columns:
            rendered_options = []
            for option in options:
                keywords = _tool_keywords(option)
                mark = "[x]" if keywords and _matches_keywords(detected, keywords) else "[ ]"
                rendered_options.append(f"{mark} {option}")
            cells.append("<br>".join(_escape_cell(item) for item in rendered_options))
        lines.append(f"| {_escape_cell(section_name)} | " + " | ".join(cells) + " |")
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def _render_parameters(rows: list[dict]) -> str:
    lines = [
        "## 5. Agent 동작 필수 파라미터 (Parameters)",
        "",
        "| 시스템 | 파라미터 | 값 / 설명 |",
        "|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {_escape_cell(row['system'])} | {_escape_cell(row['name'])} | {_escape_cell(row['value'])} |")
    if not rows:
        lines.append("| 확인 필요 | 확인 필요 | 확인 필요 |")
    lines.append("")
    return "\n".join(lines)


def render_markdown(document: dict) -> str:
    context_text = _collect_document_context(document)
    parts = [f"# {document['title']}", ""]
    parts.append(_render_simple_bullets("작성 배경", document["background"]))
    parts.append(_render_simple_bullets("목적", document["purpose"]))
    parts.append(_render_simple_bullets("비고", document["writing_notes"]))
    parts.append("")
    parts.append("## 문서 목차")
    parts.append("")
    toc_items = [
        "개요 (Overview)",
        "Agent 유형 분류 (Classification)",
        "업무 Flow 변화 & 구현 방안 (Work Process)",
        "운영 Tool 리스트 (Tool List)",
        "Agent 동작 필수 파라미터 (Parameters)",
        "기타 참고사항 및 제약조건",
    ]
    for index, item in enumerate(toc_items, start=1):
        parts.append(f"{index}. {item}")
    parts.append("")

    parts.append(_render_overview(document["overview"]))
    parts.append(_render_classification(document["classification"], context_text))
    parts.append(_render_work_process(document["work_process"]))
    parts.append(_render_tools(document["tools"], context_text))
    parts.append(_render_parameters(document["parameters"]))

    parts.append("## 6. 기타 참고사항 및 제약조건\n")
    for item in document["considerations"]:
        parts.append(f"- {item}")
    if not document["considerations"]:
        parts.append("- 확인 필요")
    parts.append("")

    parts.append("## Assumptions\n")
    for item in document["assumptions"]:
        parts.append(f"- {item}")
    if not document["assumptions"]:
        parts.append("- 없음")
    parts.append("")

    return "\n".join(parts).strip() + "\n"


def _render_flow_block(flow: dict) -> str:
    parts: list[str] = []
    if flow["title"]:
        parts.append(f"제목: {_escape_cell(flow['title'])}")
    if flow["actors"]:
        parts.append("참여자: " + ", ".join(_escape_cell(item) for item in flow["actors"]))
    if flow["steps"]:
        parts.append("흐름: " + " -> ".join(_escape_cell(item) for item in flow["steps"]))
    if flow["outputs"]:
        parts.append("출력: " + ", ".join(_escape_cell(item) for item in flow["outputs"]))
    return "<br>".join(parts) if parts else "확인 필요"


def _render_architecture(components: list[dict]) -> str:
    if not components:
        return "확인 필요"
    rendered = []
    for item in components:
        role_text = ", ".join(_escape_cell(role) for role in item["roles"]) if item["roles"] else "확인 필요"
        rendered.append(f"{_escape_cell(item['name'])}: {role_text}")
    return "<br>".join(rendered)


def _collect_classification_text(groups: list[dict]) -> str:
    fragments: list[str] = []
    for group in groups:
        fragments.append(str(group.get("category", "")))
        for option in group.get("options", []):
            if option.get("checked"):
                fragments.append(str(option.get("label", "")))
                fragments.append(str(option.get("note", "")))
    return " ".join(fragments).lower()


def _collect_tool_text(rows: list[dict]) -> str:
    fragments: list[str] = []
    for row in rows:
        if row.get("used"):
            fragments.extend([str(row.get("category", "")), str(row.get("system", "")), str(row.get("purpose", ""))])
    return " ".join(fragments).lower()


def _matches_keywords(haystack: str, keywords: list[str]) -> bool:
    return any(keyword.lower() in haystack for keyword in keywords)


def _tool_keywords(option: str) -> list[str]:
    mapping = {
        "Work Portal": ["work portal"],
        "통풍감": ["통풍감"],
        "MCMP": ["mcmp"],
        "OPMATE": ["opmate"],
        "ServiceFlow": ["serviceflow"],
        "ServiceNow": ["servicenow"],
        "Jira": ["jira"],
        "Confluence": ["confluence"],
        "Slack": ["slack"],
        "Email": ["email", "mail"],
        "SMS": ["sms"],
        "AirTable": ["airtable"],
        "GitLab": ["gitlab"],
        "Splunk": ["splunk"],
        "AMON": ["amon"],
        "Datadog": ["datadog"],
        "AnyCatcher (On-Prem)": ["anycatcher"],
        "Ontune (On-Prem)": ["ontune"],
        "Ontune (k8s)": ["ontune", "k8s"],
        "Prometheus": ["prometheus"],
        "Grafana": ["grafana"],
        "Sherpa": ["sherpa"],
        "Pinpoint": ["pinpoint"],
        "EnPharos": ["enpharos"],
        "NMS": ["nms"],
        "Telenet Center": ["telenet center"],
        "DCIM": ["dcim"],
        "...": [],
    }
    return mapping.get(option, [option.lower()])


def _collect_document_context(document: dict) -> str:
    parts: list[str] = [str(document.get("title", ""))]
    for section in ("background", "purpose", "writing_notes", "considerations", "assumptions"):
        parts.extend(str(item) for item in document.get(section, []))
    for row in document.get("overview", []):
        parts.append(str(row.get("label", "")))
        parts.append(str(row.get("value", "")))
    work = document.get("work_process", {})
    if work:
        parts.append(str(work.get("sample_flow_document", "")))
        parts.append(str(work.get("sharepoint_link", "")))
        parts.extend(str(item) for item in work.get("file_naming", []))
        for flow_key in ("as_is", "to_be"):
            flow = work.get(flow_key, {})
            parts.append(str(flow.get("title", "")))
            parts.extend(str(item) for item in flow.get("actors", []))
            parts.extend(str(item) for item in flow.get("steps", []))
            parts.extend(str(item) for item in flow.get("outputs", []))
        for comp in work.get("implementation_architecture", []):
            parts.append(str(comp.get("name", "")))
            parts.extend(str(item) for item in comp.get("roles", []))
        for step in work.get("implementation_steps", []):
            parts.append(str(step.get("stage", "")))
            parts.extend(str(item) for item in step.get("details", []))
    for row in document.get("tools", []):
        parts.append(str(row.get("category", "")))
        parts.append(str(row.get("system", "")))
        parts.append(str(row.get("purpose", "")))
    for row in document.get("parameters", []):
        parts.append(str(row.get("system", "")))
        parts.append(str(row.get("name", "")))
        parts.append(str(row.get("value", "")))
    return " ".join(parts).lower()
