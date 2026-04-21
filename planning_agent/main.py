from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from openai import OpenAI

from planning_agent.analyzer import summarize_codebase
from planning_agent.prompts import SYSTEM_PROMPT, build_user_prompt
from planning_agent.render import render_markdown
from planning_agent.schema import build_schema


def _load_env_file() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="코드베이스를 분석해 Agent 기획서 형식의 Markdown 문서를 생성합니다."
    )
    parser.add_argument("--source", required=True, help="분석할 코드 또는 프로젝트 폴더 경로")
    parser.add_argument("--output", default="agent_planning_doc.md", help="생성할 Markdown 파일 경로")
    parser.add_argument("--html-output", help="생성할 HTML 파일 경로")
    parser.add_argument("--project-name", help="문서에 표시할 프로젝트명")
    parser.add_argument(
        "--purpose",
        default="코드를 기반으로 Agent 목적과 운영 구조를 문서화",
        help="이 Agent의 비즈니스 목적",
    )
    parser.add_argument("--context", default="", help="추가 설명 또는 운영 배경")
    parser.add_argument(
        "--model",
        default=os.getenv("AZURE_OPENAI_MODEL")
        or os.getenv("OPENAI_MODEL")
        or "gpt-4.1-mini",
        help="사용할 모델 또는 Azure Deployment 이름",
    )
    return parser


def _build_client() -> OpenAI:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if azure_endpoint and azure_api_key:
        base_url = f"{azure_endpoint.rstrip('/')}/openai/v1/"
        return OpenAI(api_key=azure_api_key, base_url=base_url)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return OpenAI(api_key=openai_api_key)

    raise RuntimeError(
        "환경변수가 필요합니다. "
        "Azure 사용 시 AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_MODEL을 설정하세요. "
        "OpenAI 사용 시 OPENAI_API_KEY, OPENAI_MODEL을 설정하세요."
    )


def generate_document(args: argparse.Namespace) -> tuple[dict, str]:
    summary = summarize_codebase(args.source)

    project_name = args.project_name or summary.project_name
    prompt = build_user_prompt(
        project_name=project_name,
        business_goal=args.purpose,
        extra_context=args.context,
        code_summary=summary.summary_text,
    )

    schema = build_schema()
    client = _build_client()
    response = client.responses.create(
        model=args.model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
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
    markdown = render_markdown(payload)
    return payload, markdown


def main() -> int:
    _load_env_file()
    parser = _build_parser()
    args = parser.parse_args()

    _, markdown = generate_document(args)
    output_path = Path(args.output).resolve()
    output_path.write_text(markdown, encoding="utf-8")
    if args.html_output:
        from planning_agent.html_export import markdown_to_confluence_html

        html_path = Path(args.html_output).resolve()
        html_path.write_text(markdown_to_confluence_html(markdown, title=output_path.stem), encoding="utf-8")
        print(f"HTML 생성 완료: {html_path}")
    print(f"문서 생성 완료: {output_path}")
    return 0
