from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from planning_agent.analyzer import summarize_codebase
from planning_agent.html_export import markdown_to_confluence_html
from planning_agent.main import _build_client, _load_env_file
from planning_agent.validation_schema import build_validation_schema


VALIDATION_SYSTEM_PROMPT = """당신은 기획서와 구현 코드를 비교해 기능 적합도를 검증하는 리뷰어입니다.

반드시 지켜야 할 규칙:
1. 출력은 JSON 스키마만 따릅니다.
2. 한국어로 작성합니다.
3. 코드에 없는 기능을 있다고 추정하지 않습니다.
4. evidence에는 코드 요약에서 확인 가능한 근거만 짧게 적습니다.
5. score는 0~100 범위입니다.
6. verdict는 높음, 중간, 낮음 중 하나입니다.
7. section_scores는 최소한 개요, 유형 분류, Work Process, Tool List, Parameters 기준으로 평가합니다.
8. requirement_checks는 기획서에서 중요한 요구사항을 5~10개 추려서 충족 여부를 평가합니다.
9. major_risks에는 실제 구현 누락, 애매한 부분, 운영 리스크를 적습니다.
10. recommended_actions에는 구현 보완이나 재검증 방법을 적습니다.
"""


def build_validation_prompt(*, planning_text: str, code_summary: str) -> str:
    return f"""다음 기획서와 코드 요약을 비교해서, 코드가 기획서를 얼마나 충족하는지 검증 리포트를 작성하세요.

[기획서]
{planning_text}

[코드 요약]
{code_summary}

평가 기준:
- 기능 적합도
- 워크플로우 충족도
- Tool 사용 일치도
- 필수 파라미터 반영 여부
- 구현 누락 및 리스크
"""


def render_validation_markdown(report: dict, plan_path: str, code_path: str) -> str:
    lines = [
        f"# {report['title']}",
        "",
        f"- 기획서: `{Path(plan_path).resolve()}`",
        f"- 코드 경로: `{Path(code_path).resolve()}`",
        f"- 종합 적합도: `{report['overall_score']}%`",
        f"- 판정: `{report['verdict']}`",
        "",
        f"{report['summary']}",
        "",
        "## 섹션별 평가",
        "",
        "| 섹션 | 점수 | 상태 | 요약 |",
        "|---|---|---|---|",
    ]

    for item in report["section_scores"]:
        lines.append(
            f"| {item['section']} | {item['score']} | {item['status']} | {item['summary'].replace('|', '\\|')} |"
        )

    lines.append("")
    lines.append("## 주요 요구사항 체크")
    lines.append("")
    lines.append("| 요구사항 | 충족 여부 | 신뢰도 | 비고 |")
    lines.append("|---|---|---|---|")
    for item in report["requirement_checks"]:
        satisfied = "O" if item["satisfied"] else "X"
        lines.append(
            f"| {item['requirement'].replace('|', '\\|')} | {satisfied} | {item['confidence']} | {item['notes'].replace('|', '\\|')} |"
        )
        if item["evidence"]:
            lines.append(f"|  |  |  | 근거: {'<br>'.join(e.replace('|', '\\|') for e in item['evidence'])} |")

    lines.append("")
    lines.append("## 주요 리스크")
    lines.append("")
    if report["major_risks"]:
        for item in report["major_risks"]:
            lines.append(f"- {item}")
    else:
        lines.append("- 없음")

    lines.append("")
    lines.append("## 권장 조치")
    lines.append("")
    if report["recommended_actions"]:
        for item in report["recommended_actions"]:
            lines.append(f"- {item}")
    else:
        lines.append("- 없음")
    lines.append("")
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="기획서 기준 코드 기능 적합도를 검증합니다.")
    parser.add_argument("--plan", required=True, help="기준 기획서 Markdown 파일 경로")
    parser.add_argument("--source", required=True, help="검증할 코드 또는 폴더 경로")
    parser.add_argument("--output-md", default="spec_validation_report.md", help="Markdown 리포트 출력 경로")
    parser.add_argument("--output-json", default="spec_validation_report.json", help="JSON 리포트 출력 경로")
    parser.add_argument("--output-html", help="HTML 리포트 출력 경로")
    parser.add_argument(
        "--model",
        default=os.getenv("AZURE_OPENAI_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini",
        help="사용할 모델 또는 Azure Deployment 이름",
    )
    return parser


def generate_validation_report(plan_path: str, source_path: str, model: str) -> tuple[dict, str]:
    planning_text = Path(plan_path).resolve().read_text(encoding="utf-8")
    code_summary = summarize_codebase(source_path, max_files=40, max_chars_per_file=3000).summary_text
    prompt = build_validation_prompt(planning_text=planning_text, code_summary=code_summary)
    schema = build_validation_schema()
    client = _build_client()
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": schema["name"],
                "strict": True,
                "schema": schema["schema"],
            }
        },
    )
    payload = json.loads(response.output_text)
    markdown = render_validation_markdown(payload, plan_path, source_path)
    return payload, markdown


def main() -> int:
    _load_env_file()
    parser = _build_parser()
    args = parser.parse_args()

    payload, markdown = generate_validation_report(args.plan, args.source, args.model)

    output_md = Path(args.output_md).resolve()
    output_json = Path(args.output_json).resolve()
    output_md.write_text(markdown, encoding="utf-8")
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.output_html:
        output_html = Path(args.output_html).resolve()
        output_html.write_text(markdown_to_confluence_html(markdown, title=output_md.stem), encoding="utf-8")
        print(f"HTML 검증 리포트 생성 완료: {output_html}")

    print(f"검증 리포트 생성 완료: {output_md}")
    return 0
