# RepoWarden

RepoWarden es una herramienta de línea de comandos escrita en Python sin dependencias externas. Inspecciona un repositorio local y genera un informe sobre su estructura, lenguajes, estado de Git, tamaño y señales básicas de mantenimiento.

## Instalación

Requiere Python 3.9 o posterior.

```bash
git clone https://github.com/Xyraniz/RepoWarden.git
cd RepoWarden
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

También puede ejecutarse directamente con `PYTHONPATH=src`.

## Uso

```bash
repowarden .
repowarden ~/proyectos/mi-app --output report.md
repowarden . --format json --output report.json
```

El informe recoge archivos y líneas por extensión, rama y último commit, cambios pendientes, presencia de README, licencia, pruebas y GitHub Actions, además de los cinco archivos más grandes. Markdown está pensado para lectura humana; JSON, para scripts y automatizaciones.

## Desarrollo

La implementación está en `src/`, las pruebas en `tests/` y la configuración del paquete en `pyproject.toml`. RepoWarden no interpreta la calidad del código ni reemplaza una auditoría: sus señales describen lo que encuentra en el árbol local.
