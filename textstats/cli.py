"""Command line interface: python -m textstats FILE [--top N]."""

import argparse
import sys

from textstats.core import count_text
from textstats.frequency import top_words


def non_negative(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be 0 or more")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="textstats", description="Report statistics about a text file.")
    parser.add_argument("file", help="text file to read, or - for standard input")
    parser.add_argument("--top", type=non_negative, default=5, metavar="N", help="show the N most frequent words (default 5, 0 to hide)")
    parser.add_argument("--keep-stopwords", action="store_true", help="count common words such as 'the' too")
    return parser


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = read_text(args.file)
    except OSError as err:
        print(f"textstats: {err}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"textstats: {args.file} is not UTF-8 text", file=sys.stderr)
        return 1

    counts = count_text(text)
    print(f"lines:      {counts.lines}")
    print(f"words:      {counts.words}")
    print(f"characters: {counts.characters}")

    words = top_words(text, args.top, ignore_stopwords=not args.keep_stopwords)
    if words:
        print("top words:")
        for word, count in words:
            print(f"  {count:>4}  {word}")
    return 0
