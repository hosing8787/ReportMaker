from __future__ import annotations

import argparse
import json
import os
import unittest
from unittest.mock import MagicMock, patch

from planning_agent import main as main_module


class MainTests(unittest.TestCase):
    def test_load_env_file_populates_missing_values_only(self) -> None:
        env_content = (
            "AZURE_OPENAI_ENDPOINT=https://example.openai.azure.com/\n"
            "AZURE_OPENAI_MODEL=gpt-4.1-mini\n"
        )
        os.environ.pop("AZURE_OPENAI_ENDPOINT", None)
        os.environ["AZURE_OPENAI_MODEL"] = "keep-existing"

        try:
            with patch("planning_agent.main.Path.exists", return_value=True):
                with patch("planning_agent.main.Path.read_text", return_value=env_content):
                    main_module._load_env_file()

            self.assertEqual(os.environ["AZURE_OPENAI_ENDPOINT"], "https://example.openai.azure.com/")
            self.assertEqual(os.environ["AZURE_OPENAI_MODEL"], "keep-existing")
        finally:
            os.environ.pop("AZURE_OPENAI_ENDPOINT", None)
            os.environ.pop("AZURE_OPENAI_MODEL", None)

    def test_build_client_prefers_azure_configuration(self) -> None:
        with patch.dict(
            os.environ,
            {
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
                "AZURE_OPENAI_API_KEY": "azure-key",
                "OPENAI_API_KEY": "openai-key",
            },
            clear=False,
        ):
            with patch("planning_agent.main.OpenAI") as openai_cls:
                client = main_module._build_client()

        self.assertIs(client, openai_cls.return_value)
        openai_cls.assert_called_once_with(
            api_key="azure-key",
            base_url="https://example.openai.azure.com/openai/v1/",
        )

    def test_build_client_uses_openai_when_azure_is_missing(self) -> None:
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "openai-key",
            },
            clear=True,
        ):
            with patch("planning_agent.main.OpenAI") as openai_cls:
                client = main_module._build_client()

        self.assertIs(client, openai_cls.return_value)
        openai_cls.assert_called_once_with(api_key="openai-key")

    def test_generate_document_returns_payload_and_markdown(self) -> None:
        payload = {
            "title": "문서",
            "background": ["배경"],
            "purpose": ["목적"],
            "writing_notes": ["비고"],
            "toc": ["개요"],
            "overview": [{"label": "개요", "value": "설명"}],
            "classification": [
                {
                    "category": "유형",
                    "options": [{"label": "자동", "checked": True, "note": ""}],
                }
            ],
            "work_process": {
                "sample_flow_document": "sample.pptx",
                "sharepoint_link": "확인 필요",
                "file_naming": ["Rule : sample"],
                "as_is": {"title": "현재", "actors": ["운영자"], "steps": ["수집"], "outputs": ["메일"]},
                "to_be": {"title": "목표", "actors": ["운영자", "Agent"], "steps": ["자동화"], "outputs": ["Slack"]},
                "implementation_architecture": [{"name": "Core Agent", "roles": ["제어"]}],
                "implementation_steps": [{"stage": "1단계", "details": ["요청 입력"]}],
            },
            "tools": [{"category": "AI", "system": "Azure", "used": True, "purpose": "생성"}],
            "parameters": [{"system": "Azure", "name": "param", "value": "x"}],
            "considerations": ["주의"],
            "assumptions": ["가정"],
        }
        args = argparse.Namespace(
            source="C:/repo",
            project_name="프로젝트",
            purpose="목적",
            context="추가 맥락",
            model="gpt-4.1-mini",
        )

        fake_response = MagicMock()
        fake_response.output_text = json.dumps(payload, ensure_ascii=False)
        fake_client = MagicMock()
        fake_client.responses.create.return_value = fake_response

        with patch("planning_agent.main.summarize_codebase") as summarize_mock:
            summarize_mock.return_value.project_name = "repo"
            summarize_mock.return_value.summary_text = "코드 요약"

            with patch("planning_agent.main._build_client", return_value=fake_client):
                result_payload, markdown = main_module.generate_document(args)

        self.assertEqual(result_payload, payload)
        self.assertIn("# 문서", markdown)
        fake_client.responses.create.assert_called_once()
        call_kwargs = fake_client.responses.create.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "gpt-4.1-mini")
        self.assertEqual(call_kwargs["text"]["format"]["type"], "json_schema")


if __name__ == "__main__":
    unittest.main()
