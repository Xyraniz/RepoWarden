"""Repository inspection and report data generation."""
from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

LANGUAGE_BY_SUFFIX = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".jsx": "JavaScript", ".lua": "Lua", ".html": "HTML", ".css": "CSS",
    ".scss": "SCSS", ".go": "Go", ".rs": "Rust", ".java": "Java",
    ".c": "C", ".h": "C", ".cpp": "C++", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".sh": "Shell", ".sql": "SQL", ".md": "Markdown",
    ".yml": "YAML", ".yaml": "YAML", ".json": "JSON",
}
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}

@dataclass
class RepositoryReport:
    name: str
    path: str
    is_git_repository: bool
    total_files: int
    total_lines: int
    languages: Dict[str, int]
    largest_files: List[Dict[str, int | str]]
    has_readme: bool
    has_license: bool
    has_tests: bool
    has_ci: bool
    branch: Optional[str]
    last_commit: Optional[str]
    git_status: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and not any(part in IGNORED_DIRS for part in path.parts):
            yield path


def _git(root: Path, *args: str) -> Optional[str]:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def analyze_repository(path: str | Path) -> RepositoryReport:
    root = Path(path).expanduser().resolve()
    files = list(_iter_files(root)) if root.exists() else []
    languages: Dict[str, int] = {}
    sizes: List[Dict[str, int | str]] = []
    total_lines = 0
    for file in files:
        suffix = file.suffix.lower()
        language = LANGUAGE_BY_SUFFIX.get(suffix)
        if language:
            languages[language] = languages.get(language, 0) + 1
        try:
            data = file.read_bytes()
            lines = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
            total_lines += lines
            sizes.append({"path": str(file.relative_to(root)), "bytes": len(data), "lines": lines})
        except OSError:
            continue
    sizes.sort(key=lambda item: int(item["bytes"]), reverse=True)
    git_dir = root / ".git"
    status = _git(root, "status", "--short") if git_dir.exists() else None
    return RepositoryReport(
        name=root.name,
        path=str(root),
        is_git_repository=git_dir.exists(),
        total_files=len(files),
        total_lines=total_lines,
        languages=dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)),
        largest_files=sizes[:5],
        has_readme=any((root / name).exists() for name in ("README.md", "README.rst", "README.txt")),
        has_license=any(root.glob("LICENSE*")),
        has_tests=(root / "tests").is_dir() or any("test" in p.name.lower() for p in files),
        has_ci=(root / ".github" / "workflows").is_dir(),
        branch=_git(root, "branch", "--show-current") if git_dir.exists() else None,
        last_commit=_git(root, "log", "-1", "--format=%h %s") if git_dir.exists() else None,
        git_status=status if status else ("clean" if git_dir.exists() else None),
    )


def report_as_json(report: RepositoryReport) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
