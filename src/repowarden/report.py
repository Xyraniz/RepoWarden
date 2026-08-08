"""Human-readable report rendering."""
from __future__ import annotations

from .analyzer import RepositoryReport


def _language_rows(report: RepositoryReport) -> str:
    if not report.languages:
        return "| — | 0 |\n|---|---:|"
    return "\n".join(f"| {name} | {count} |" for name, count in report.languages.items())


def render_markdown(report: RepositoryReport) -> str:
    status = report.git_status or "No es un repositorio Git"
    languages = ", ".join(report.languages) if report.languages else "No detectados"
    largest = "\n".join(
        f"| `{item['path']}` | {item['lines']} | {item['bytes']:,} |" for item in report.largest_files
    ) or "| — | 0 | 0 |"
    return f"""# Informe de RepoWarden: {report.name}

> Informe generado automáticamente para inspeccionar la salud y composición de un repositorio local.

## Resumen

| Métrica | Resultado |
|---|---:|
| Archivos analizados | {report.total_files} |
| Líneas totales | {report.total_lines:,} |
| Repositorio Git | {'Sí' if report.is_git_repository else 'No'} |
| Rama actual | `{report.branch or '—'}` |
| Estado | `{status}` |
| README | {'Sí' if report.has_readme else 'No'} |
| Licencia | {'Sí' if report.has_license else 'No'} |
| Pruebas | {'Sí' if report.has_tests else 'No'} |
| CI configurada | {'Sí' if report.has_ci else 'No'} |

## Lenguajes detectados

Lenguajes presentes: **{languages}**.

| Lenguaje | Archivos |
|---|---:|
{_language_rows(report)}

## Archivos más grandes

| Archivo | Líneas | Bytes |
|---|---:|---:|
{largest}

## Último commit

`{report.last_commit or 'No disponible'}`

---

Generado con [RepoWarden](https://github.com/Xyraniz/repowarden).
"""
