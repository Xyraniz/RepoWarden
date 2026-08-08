"""Command-line interface for RepoWarden."""
from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_repository, report_as_json
from .report import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repowarden",
        description="Analiza un repositorio local y crea un informe de composición y salud.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Ruta del repositorio que se analizará (por defecto: .)")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Formato de salida")
    parser.add_argument("--output", "-o", type=Path, help="Archivo de salida; si se omite, imprime en pantalla")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target = Path(args.path).expanduser()
    if not target.exists() or not target.is_dir():
        print(f"Error: la ruta no existe o no es un directorio: {target}")
        return 2
    report = analyze_repository(target)
    content = report_as_json(report) if args.format == "json" else render_markdown(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n", encoding="utf-8")
        print(f"Informe guardado en {args.output}")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
