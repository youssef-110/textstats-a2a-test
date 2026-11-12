import re
from collections import Counter

# Runs of Unicode letters/digits, plus apostrophes.
_WORD_RE = re.compile(r"(?:[^\W_]|')+")

STOPWORDS = frozenset({
    "a", "about", "above", "after", "again", "all", "am", "an", "and", "any",
    "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "could", "did", "do", "does",
    "doing", "down", "during", "each", "few", "for", "from", "further", "had",
    "has", "have", "having", "he", "her", "here", "hers", "him", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "just", "me", "more", "most",
    "my", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or",
    "other", "our", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "them", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "will", "with", "would", "you", "your",
})


def top_words(text: str, n: int = 10, ignore_stopwords: bool = True) -> list[tuple[str, int]]:
    """Return the n most frequent words in text as (word, count) pairs.

    Matching is case-insensitive. Words are runs of letters, digits and
    apostrophes. Results are sorted by count descending, then alphabetically.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, not {type(text).__name__}")
    if n <= 0:
        return []

    counts: Counter[str] = Counter()
    for match in _WORD_RE.finditer(text.lower()):
        word = match.group().strip("'")
        if not word:
            continue
        if ignore_stopwords and word in STOPWORDS:
            continue
        counts[word] += 1

    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]
