import json
import tempfile
import unittest
from pathlib import Path

from repowarden.analyzer import analyze_repository, report_as_json
from repowarden.cli import main
from repowarden.report import render_markdown


class RepoWardenTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "src").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "README.md").write_text("# Demo\n", encoding="utf-8")
        (self.root / "src" / "app.py").write_text("print('hello')\nprint('world')\n", encoding="utf-8")
        (self.root / "src" / "app.ts").write_text("export const answer = 42;\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_analyze_counts_files_lines_and_languages(self):
        report = analyze_repository(self.root)
        self.assertEqual(report.total_files, 3)
        self.assertEqual(report.total_lines, 4)
        self.assertEqual(report.languages["Python"], 1)
        self.assertEqual(report.languages["TypeScript"], 1)
        self.assertTrue(report.has_readme)
        self.assertTrue(report.has_tests)

    def test_json_is_serializable(self):
        payload = json.loads(report_as_json(analyze_repository(self.root)))
        self.assertEqual(payload["name"], self.root.name)
        self.assertIn("languages", payload)

    def test_markdown_contains_summary(self):
        markdown = render_markdown(analyze_repository(self.root))
        self.assertIn("# Informe de RepoWarden", markdown)
        self.assertIn("Archivos analizados", markdown)
        self.assertIn("Python", markdown)

    def test_cli_writes_json(self):
        output = self.root / "report.json"
        exit_code = main([str(self.root), "--format", "json", "--output", str(output)])
        self.assertEqual(exit_code, 0)
        self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
