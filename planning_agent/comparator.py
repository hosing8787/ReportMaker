from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from planning_agent.analyzer import collect_code_files, read_text_excerpt


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


@dataclass
class FileFeatures:
    relative_path: str
    extension: str
    tokens: set[str]
    imports: set[str]
    functions: set[str]
    classes: set[str]
    calls: set[str]
    normalized_text: str


@dataclass
class ComparisonResult:
    overall_score: float
    verdict: str
    metrics: dict[str, float]
    summary: dict[str, list[str]]


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def _normalize_text(text: str) -> str:
    lowered = text.lower()
    compact = re.sub(r"\s+", " ", lowered)
    return compact.strip()


def _extract_tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def _extract_python_features(text: str) -> tuple[set[str], set[str], set[str], set[str]]:
    imports: set[str] = set()
    functions: set[str] = set()
    classes: set[str] = set()
    calls: set[str] = set()

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return imports, functions, classes, calls

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                calls.add(func.attr)

    return imports, functions, classes, calls


def _build_features(source: str, max_files: int = 100, max_chars_per_file: int = 12000) -> tuple[Path, list[FileFeatures]]:
    base_dir, files = collect_code_files(source)
    files = sorted(files, key=lambda item: (len(item.parts), str(item)))[:max_files]
    features: list[FileFeatures] = []

    for path in files:
        text = read_text_excerpt(path, max_chars=max_chars_per_file)
        imports: set[str] = set()
        functions: set[str] = set()
        classes: set[str] = set()
        calls: set[str] = set()
        if path.suffix.lower() == ".py":
            imports, functions, classes, calls = _extract_python_features(text)

        features.append(
            FileFeatures(
                relative_path=str(path.relative_to(base_dir)).replace("\\", "/"),
                extension=path.suffix.lower() or path.name.lower(),
                tokens=_extract_tokens(text),
                imports=imports,
                functions=functions,
                classes=classes,
                calls=calls,
                normalized_text=_normalize_text(text),
            )
        )

    return base_dir, features


def compare_sources(source_a: str, source_b: str) -> ComparisonResult:
    _, left_files = _build_features(source_a)
    _, right_files = _build_features(source_b)

    left_paths = {item.relative_path for item in left_files}
    right_paths = {item.relative_path for item in right_files}
    left_exts = {item.extension for item in left_files}
    right_exts = {item.extension for item in right_files}

    left_tokens = set().union(*(item.tokens for item in left_files)) if left_files else set()
    right_tokens = set().union(*(item.tokens for item in right_files)) if right_files else set()
    left_imports = set().union(*(item.imports for item in left_files)) if left_files else set()
    right_imports = set().union(*(item.imports for item in right_files)) if right_files else set()
    left_functions = set().union(*(item.functions for item in left_files)) if left_files else set()
    right_functions = set().union(*(item.functions for item in right_files)) if right_files else set()
    left_classes = set().union(*(item.classes for item in left_files)) if left_files else set()
    right_classes = set().union(*(item.classes for item in right_files)) if right_files else set()
    left_calls = set().union(*(item.calls for item in left_files)) if left_files else set()
    right_calls = set().union(*(item.calls for item in right_files)) if right_files else set()

    file_overlap = _jaccard(left_paths, right_paths)
    extension_overlap = _jaccard(left_exts, right_exts)
    token_overlap = _jaccard(left_tokens, right_tokens)
    import_overlap = _jaccard(left_imports, right_imports)
    function_overlap = _jaccard(left_functions, right_functions)
    class_overlap = _jaccard(left_classes, right_classes)
    call_overlap = _jaccard(left_calls, right_calls)

    ast_overlap = (import_overlap + function_overlap + class_overlap + call_overlap) / 4
    left_text = "\n".join(item.normalized_text for item in left_files)
    right_text = "\n".join(item.normalized_text for item in right_files)
    text_similarity = SequenceMatcher(a=left_text, b=right_text).ratio() if left_text or right_text else 1.0

    overall_score = (
        file_overlap * 0.15
        + extension_overlap * 0.10
        + token_overlap * 0.35
        + ast_overlap * 0.20
        + text_similarity * 0.20
    ) * 100

    if overall_score >= 80:
        verdict = "높음"
    elif overall_score >= 55:
        verdict = "중간"
    else:
        verdict = "낮음"

    summary = {
        "공통 파일": sorted(left_paths & right_paths)[:10],
        "원본에만 있는 파일": sorted(left_paths - right_paths)[:10],
        "비교대상에만 있는 파일": sorted(right_paths - left_paths)[:10],
        "공통 import": sorted(left_imports & right_imports)[:10],
        "공통 함수": sorted(left_functions & right_functions)[:10],
        "공통 호출": sorted(left_calls & right_calls)[:10],
    }

    metrics = {
        "file_overlap": round(file_overlap * 100, 2),
        "extension_overlap": round(extension_overlap * 100, 2),
        "token_overlap": round(token_overlap * 100, 2),
        "ast_overlap": round(ast_overlap * 100, 2),
        "text_similarity": round(text_similarity * 100, 2),
    }

    return ComparisonResult(
        overall_score=round(overall_score, 2),
        verdict=verdict,
        metrics=metrics,
        summary=summary,
    )


def render_comparison_markdown(result: ComparisonResult, source_a: str, source_b: str) -> str:
    lines = [
        "# 코드 기능 유사도 비교 리포트",
        "",
        f"- 원본 코드: `{Path(source_a).resolve()}`",
        f"- 비교 대상 코드: `{Path(source_b).resolve()}`",
        f"- 종합 유사도: `{result.overall_score}%`",
        f"- 판정: `{result.verdict}`",
        "",
        "## 세부 지표",
        "",
        "| 지표 | 점수 |",
        "|---|---|",
    ]

    for key, value in result.metrics.items():
        lines.append(f"| {key} | {value}% |")

    lines.append("")
    lines.append("## 주요 공통점/차이")
    lines.append("")

    for title, items in result.summary.items():
        lines.append(f"### {title}")
        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append("- 없음")
        lines.append("")

    lines.append("## 해석 가이드")
    lines.append("")
    lines.append("- 이 점수는 기능 동등성의 증명은 아니고, 구조와 구현 신호를 바탕으로 한 휴리스틱 추정치입니다.")
    lines.append("- 특히 파일명, 함수명, import 구조가 많이 다르지만 실제 기능은 비슷한 경우 점수가 낮게 나올 수 있습니다.")
    lines.append("- 반대로 이름과 구조가 비슷해도 내부 로직 차이가 크면 실제 기능 차이는 더 클 수 있습니다.")
    lines.append("")
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="두 코드 또는 저장소의 기능 유사도를 비교합니다.")
    parser.add_argument("--source-a", required=True, help="기준 코드 또는 폴더 경로")
    parser.add_argument("--source-b", required=True, help="비교 대상 코드 또는 폴더 경로")
    parser.add_argument("--output", default="code_similarity_report.md", help="리포트 저장 경로")
    parser.add_argument("--json-output", help="JSON 결과 저장 경로")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    result = compare_sources(args.source_a, args.source_b)
    markdown = render_comparison_markdown(result, args.source_a, args.source_b)
    output_path = Path(args.output).resolve()
    output_path.write_text(markdown, encoding="utf-8")

    if args.json_output:
        json_path = Path(args.json_output).resolve()
        json_path.write_text(
            json.dumps(
                {
                    "overall_score": result.overall_score,
                    "verdict": result.verdict,
                    "metrics": result.metrics,
                    "summary": result.summary,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"비교 리포트 생성 완료: {output_path}")
    return 0
