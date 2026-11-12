import pytest

from textstats import count_text
from textstats.frequency import top_words


@pytest.mark.parametrize("text", [
    "The cat sat. The cat ran!",
    "café naïve 'quoted' don't ''",
    "one\ntwo\tthree -- four_five 6",
    "",
])
def test_word_count_matches_frequency_total(text):
    # Both parts must agree on what a word is: the total of the frequency
    # list, with nothing filtered out, is the word count.
    everything = top_words(text, 10_000, ignore_stopwords=False)
    assert sum(count for _, count in everything) == count_text(text).words
