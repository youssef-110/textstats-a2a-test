"""The one rule for what a word is, shared by the counts and the frequency list."""

import re

# Runs of Unicode letters and digits, plus apostrophes inside a word.
_WORD_RE = re.compile(r"(?:[^\W_]|')+")


def find_words(text: str) -> list[str]:
    """Return the words in text, in order, as written.

    Apostrophes at the start or end of a word are dropped, so "'quoted'" is
    "quoted" and a lone apostrophe is not a word. "don't" stays one word.
    """
    words = []
    for match in _WORD_RE.finditer(text):
        word = match.group().strip("'")
        if word:
            words.append(word)
    return words
