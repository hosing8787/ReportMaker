from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".kt",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".swift",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".env",
    ".sql",
    ".md",
    ".txt",
    ".sh",
    ".ps1",
    ".dockerfile",
}

SKIP_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".next",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}


@dataclass
class CodeSummary:
    project_name: str
    file_count: int
    summary_text: str


def _is_text_file(path: Path) -> bool:
    if path.name.lower() in {"dockerfile", ".env"}:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def _read_text(path: Path, max_chars: int) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            content = path.read_text(encoding="cp949", errors="ignore")
    return content[:max_chars].strip()


def read_text_excerpt(path: Path, max_chars: int = 2500) -> str:
    return _read_text(path, max_chars=max_chars)


def collect_code_files(source: str) -> tuple[Path, list[Path]]:
    root = Path(source).resolve()
    if not root.exists():
        raise FileNotFoundError(f"소스 경로를 찾을 수 없습니다: {root}")

    if root.is_file():
        files = [root] if _is_text_file(root) else []
        return root.parent, files

    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and _is_text_file(path):
            files.append(path)
    return root, files


def summarize_codebase(source: str, max_files: int = 30, max_chars_per_file: int = 2500) -> CodeSummary:
    root = Path(source).resolve()
    base_dir, files = collect_code_files(source)

    files.sort(key=lambda item: (len(item.parts), str(item)))
    selected = files[:max_files]

    lines = [
        f"루트 경로: {root}",
        f"탐지 파일 수: {len(files)}",
        f"요약 포함 파일 수: {len(selected)}",
        "",
    ]

    for path in selected:
        rel = path.relative_to(base_dir)
        excerpt = read_text_excerpt(path, max_chars=max_chars_per_file)
        lines.append(f"### 파일: {rel}")
        lines.append(excerpt or "(비어 있음)")
        lines.append("")

    if len(files) > len(selected):
        lines.append(f"추가 파일 {len(files) - len(selected)}개는 길이 제한으로 생략됨")

    return CodeSummary(
        project_name=root.name,
        file_count=len(files),
        summary_text="\n".join(lines).strip(),
    )
