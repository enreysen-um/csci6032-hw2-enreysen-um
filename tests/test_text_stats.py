import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.text_stats import calculate_stats


class TextStatsTests(unittest.TestCase):
    repository_root = Path(__file__).resolve().parents[1]

    def test_calculate_stats_counts_unicode_text(self):
        self.assertEqual(
            calculate_stats("Hello, world!\nCafé 😊"),
            {"lines": 2, "words": 4, "characters": 20},
        )

    def test_calculate_stats_handles_empty_text(self):
        self.assertEqual(
            calculate_stats(""),
            {"lines": 0, "words": 0, "characters": 0},
        )

    def test_calculate_stats_returns_case_insensitive_top_words(self):
        self.assertEqual(
            calculate_stats("Banana apple BANANA cherry Apple", top=2),
            {
                "lines": 1,
                "words": 5,
                "characters": 32,
                "top_words": [
                    {"word": "apple", "count": 2},
                    {"word": "banana", "count": 2},
                ],
            },
        )

    def test_calculate_stats_breaks_top_word_ties_deterministically(self):
        self.assertEqual(
            calculate_stats("zulu Alpha bravo", top=3)["top_words"],
            [
                {"word": "alpha", "count": 1},
                {"word": "bravo", "count": 1},
                {"word": "zulu", "count": 1},
            ],
        )

    def test_cli_reads_utf8_file_and_prints_json(self):
        with tempfile.TemporaryDirectory(dir=self.repository_root) as directory:
            input_path = Path(directory) / "input.txt"
            input_path.write_text("one two\nthree 😊\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "src/text_stats.py", str(input_path)],
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 2, "words": 4, "characters": 16},
        )

    def test_cli_reports_requested_top_words(self):
        with tempfile.TemporaryDirectory(dir=self.repository_root) as directory:
            input_path = Path(directory) / "input.txt"
            input_path.write_text("Pear pear apple APPLE pear", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "src/text_stats.py",
                    str(input_path),
                    "--top",
                    "2",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertEqual(
            json.loads(result.stdout)["top_words"],
            [
                {"word": "pear", "count": 3},
                {"word": "apple", "count": 2},
            ],
        )

    def test_cli_rejects_negative_top(self):
        with tempfile.TemporaryDirectory(dir=self.repository_root) as directory:
            input_path = Path(directory) / "input.txt"
            input_path.write_text("word", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "src/text_stats.py",
                    str(input_path),
                    "--top",
                    "-1",
                ],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be non-negative", result.stderr)


if __name__ == "__main__":
    unittest.main()
