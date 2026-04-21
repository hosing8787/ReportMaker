from __future__ import annotations

import argparse
import html
from pathlib import Path


def _convert_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace("&lt;br&gt;", "<br>")
    return escaped


def markdown_to_confluence_html(markdown: str, title: str = "Agent Planning Document") -> str:
    lines = markdown.splitlines()
    body: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("# "):
            body.append(f"<h1>{_convert_inline(stripped[2:])}</h1>")
            i += 1
            continue

        if stripped.startswith("## "):
            body.append(f"<h2>{_convert_inline(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("### "):
            body.append(f"<h3>{_convert_inline(stripped[4:])}</h3>")
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 2:
                headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
                rows = table_lines[2:] if table_lines[1].replace("|", "").replace("-", "").strip() == "" else table_lines[1:]
                body.append('<table class="confluenceTable"><tbody>')
                body.append("<tr>")
                for header in headers:
                    body.append(f'<th class="confluenceTh"><p>{_convert_inline(header)}</p></th>')
                body.append("</tr>")
                for row in rows:
                    cells = [cell.strip() for cell in row.strip("|").split("|")]
                    body.append("<tr>")
                    for cell in cells:
                        body.append(f'<td class="confluenceTd"><p>{_convert_inline(cell)}</p></td>')
                    body.append("</tr>")
                body.append("</tbody></table>")
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
                while i < len(lines) and lines[i].startswith("  - "):
                    items.append(f"&nbsp;&nbsp;&nbsp;&nbsp;- {_convert_inline(lines[i].strip()[2:])}")
                    i += 1
            body.append("<ul>")
            for item in items:
                if item.startswith("&nbsp;"):
                    body.append(f"<li><p>{item}</p></li>")
                else:
                    body.append(f"<li><p>{_convert_inline(item)}</p></li>")
            body.append("</ul>")
            continue

        if stripped[0].isdigit() and ". " in stripped:
            items: list[str] = []
            while i < len(lines):
                current = lines[i].strip()
                if current and current[0].isdigit() and ". " in current:
                    items.append(current.split(". ", 1)[1])
                    i += 1
                else:
                    break
            body.append("<ol>")
            for item in items:
                body.append(f"<li><p>{_convert_inline(item)}</p></li>")
            body.append("</ol>")
            continue

        body.append(f"<p>{_convert_inline(stripped)}</p>")
        i += 1

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      font-family: Arial, "Malgun Gothic", sans-serif;
      line-height: 1.5;
      color: #172b4d;
      margin: 24px;
    }}
    h1, h2, h3 {{
      color: #172b4d;
    }}
    table.confluenceTable {{
      border-collapse: collapse;
      width: 100%;
      margin: 12px 0 20px;
      table-layout: fixed;
    }}
    .confluenceTh, .confluenceTd {{
      border: 1px solid #dfe1e6;
      padding: 8px;
      vertical-align: top;
      word-break: break-word;
    }}
    .confluenceTh {{
      background: #f4f5f7;
      font-weight: 700;
    }}
    p {{
      margin: 0;
    }}
    ul, ol {{
      margin: 8px 0 16px 20px;
      padding: 0;
    }}
    li {{
      margin: 4px 0;
    }}
  </style>
</head>
<body>
{''.join(body)}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown 기획서를 Confluence 붙여넣기용 HTML로 변환합니다.")
    parser.add_argument("--input", required=True, help="입력 Markdown 파일 경로")
    parser.add_argument("--output", required=True, help="출력 HTML 파일 경로")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    markdown = input_path.read_text(encoding="utf-8")
    html_text = markdown_to_confluence_html(markdown, title=input_path.stem)
    output_path.write_text(html_text, encoding="utf-8")
    print(f"HTML 변환 완료: {output_path}")
    return 0
