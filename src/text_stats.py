"""Print basic statistics for a UTF-8 text file."""

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Optional, Union


def calculate_stats(
    text: str, top: Optional[int] = None
) -> Dict[str, Union[int, list[dict[str, Union[str, int]]]]]:
    """Return line, word, and character counts for text."""
    stats: Dict[str, Union[int, list[dict[str, Union[str, int]]]]] = {
        "lines": len(text.splitlines()),
        "words": len(text.split()),
        "characters": len(text),
    }
    if top is not None:
        counts = Counter(word.casefold() for word in text.split())
        stats["top_words"] = [
            {"word": word, "count": count}
            for word, count in sorted(
                counts.items(), key=lambda item: (-item[1], item[0])
            )[:top]
        ]
    return stats


def non_negative_int(value: str) -> int:
    """Parse a non-negative integer for argparse."""
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


def main() -> None:
    """Read the requested file and print its statistics as JSON."""
    parser = argparse.ArgumentParser(
        description="Count lines, words, and characters in a UTF-8 text file."
    )
    parser.add_argument("file", type=Path, help="path to a UTF-8 text file")
    parser.add_argument(
        "--top",
        type=non_negative_int,
        help="include the N most frequent words",
    )
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    print(json.dumps(calculate_stats(text, args.top), ensure_ascii=False))


if __name__ == "__main__":
    main()
