import tempfile
import unittest
from pathlib import Path

from repowarden.analyzer import analyze_repository


class HealthScoreTests(unittest.TestCase):
    def test_missing_project_signals_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text("print('hello')\n", encoding="utf-8")
            report = analyze_repository(root)

        self.assertEqual(report.health_score, 0)
        self.assertEqual(len(report.recommendations), 5)
        self.assertTrue(any("README" in item for item in report.recommendations))

    def test_complete_project_scores_one_hundred(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "tests").mkdir()
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = analyze_repository(root)

        self.assertEqual(report.health_score, 100)
        self.assertEqual(report.recommendations, [])


if __name__ == "__main__":
    unittest.main()
