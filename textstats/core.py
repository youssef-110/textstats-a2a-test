"""Basic counts for a piece of text."""

from dataclasses import dataclass

from textstats.words import find_words


@dataclass(frozen=True)
class TextCounts:
    lines: int
    words: int
    characters: int


def count_text(text: str) -> TextCounts:
    """Count lines, words and characters in text.

    Lines are counted the way str.splitlines() splits them, which also breaks
    on form feeds and Unicode line separators, so the number can differ from
    `wc -l`. A last line without a newline counts. Characters are code points.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return TextCounts(
        lines=len(text.splitlines()),
        words=len(find_words(text)),
        characters=len(text),
    )
