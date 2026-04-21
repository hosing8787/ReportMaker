from __future__ import annotations

import unittest

from planning_agent.html_export import markdown_to_confluence_html


class HtmlExportTests(unittest.TestCase):
    def test_markdown_to_html_renders_headers_lists_and_tables(self) -> None:
        markdown = """# 제목

- 작성 배경
  - 상세 설명

## 표 섹션

| 항목 | 내용 |
|---|---|
| 이름 | 값<br>설명 |

1. 첫째
2. 둘째
"""
        html = markdown_to_confluence_html(markdown, title="sample")

        self.assertIn("<h1>제목</h1>", html)
        self.assertIn('<table class="confluenceTable">', html)
        self.assertIn("<th class=\"confluenceTh\"><p>항목</p></th>", html)
        self.assertIn("값<br>설명", html)
        self.assertIn("<ol>", html)
        self.assertIn("<ul>", html)


if __name__ == "__main__":
    unittest.main()
