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


if __name__ == "__main__":
    unittest.main()
