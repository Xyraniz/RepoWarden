# RepoWarden

[![CI](https://github.com/Xyraniz/repowarden/actions/workflows/ci.yml/badge.svg)](https://github.com/Xyraniz/repowarden/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**RepoWarden** es una herramienta de línea de comandos, escrita en Python sin dependencias externas, que inspecciona un repositorio local y genera un informe legible sobre su estructura, lenguajes, tamaño y señales básicas de mantenimiento.

El proyecto está pensado como una utilidad pequeña pero completa: tiene una interfaz CLI, salida Markdown y JSON, pruebas automatizadas, tipado, documentación y un flujo de integración continua.

## Qué analiza

| Área | Información |
|---|---|
| Composición | Archivos, líneas totales y lenguajes por extensión |
| Git | Rama actual, último commit y cambios pendientes |
| Mantenimiento | Presencia de README, licencia, pruebas y GitHub Actions |
| Tamaño | Los cinco archivos más grandes del repositorio |
| Exportación | Informe Markdown para humanos o JSON para automatizaciones |

## Instalación

RepoWarden requiere **Python 3.9 o superior** y no necesita paquetes de terceros.

```bash
git clone https://github.com/Xyraniz/repowarden.git
cd repowarden
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e .
```

## Uso rápido

Analizar la carpeta actual y mostrar el informe:

```bash
repowarden .
```

Guardar un informe Markdown:

```bash
repowarden ~/proyectos/mi-app --output report.md
```

Generar JSON para usarlo en scripts o pipelines:

```bash
repowarden . --format json --output report.json
```

También puedes ejecutarlo sin instalarlo:

```bash
PYTHONPATH=src python -m repowarden.cli .
```

## Desarrollo

```bash
python -m unittest discover -s tests -v
```

El repositorio usa únicamente la biblioteca estándar para que sea sencillo de ejecutar, estudiar y extender. Las contribuciones pueden añadir nuevos lenguajes en `LANGUAGE_BY_SUFFIX`, mejorar el análisis de Git o incorporar formatos de salida adicionales.

## Limitaciones conscientes

RepoWarden analiza archivos visibles del árbol local y omite directorios generados habitualmente, como `.git`, `node_modules`, `dist`, `build` y entornos virtuales. La detección de lenguajes se basa en extensiones, por lo que no pretende sustituir herramientas especializadas como GitHub Linguist o analizadores estáticos.

## Licencia

Distribuido bajo la licencia [MIT](LICENSE).
