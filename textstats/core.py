"""Basic counts for a piece of text."""

from dataclasses import dataclass
import re

# A word is a run of letters, digits and apostrophes, the same rule the
# frequency module uses, so both report the same words.
WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")


@dataclass(frozen=True)
class TextCounts:
    lines: int
    words: int
    characters: int


def count_text(text: str) -> TextCounts:
    """Count lines, words and characters in text."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return TextCounts(
        lines=len(text.splitlines()),
        words=len(WORD_PATTERN.findall(text)),
        characters=len(text),
    )
