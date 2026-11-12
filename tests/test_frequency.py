import pytest

from textstats.frequency import top_words


def test_basic_counting():
    text = "apple banana apple cherry banana apple"
    assert top_words(text, n=10, ignore_stopwords=False) == [
        ("apple", 3),
        ("banana", 2),
        ("cherry", 1),
    ]


def test_n_limits_results():
    text = "apple banana apple cherry banana apple"
    assert top_words(text, n=2, ignore_stopwords=False) == [("apple", 3), ("banana", 2)]


def test_case_insensitive():
    assert top_words("Apple APPLE apple", n=5, ignore_stopwords=False) == [("apple", 3)]


def test_tie_ordering_is_alphabetical():
    assert top_words("dog cat bird", n=3, ignore_stopwords=False) == [
        ("bird", 1),
        ("cat", 1),
        ("dog", 1),
    ]


def test_count_beats_alphabetical_order():
    assert top_words("zebra zebra apple", n=2, ignore_stopwords=False) == [
        ("zebra", 2),
        ("apple", 1),
    ]


def test_stopwords_ignored_by_default():
    assert top_words("the cat and the dog") == [("cat", 1), ("dog", 1)]


def test_stopwords_included_when_disabled():
    assert top_words("the cat and the dog", n=10, ignore_stopwords=False) == [
        ("the", 2),
        ("and", 1),
        ("cat", 1),
        ("dog", 1),
    ]


@pytest.mark.parametrize("n", [0, -1, -100])
def test_non_positive_n_returns_empty_list(n):
    assert top_words("apple apple banana", n=n, ignore_stopwords=False) == []


def test_empty_text_returns_empty_list():
    assert top_words("") == []


def test_only_punctuation_returns_empty_list():
    assert top_words("!!! ... --- ") == []


@pytest.mark.parametrize("bad", [None, b"apple", 123, ["apple"]])
def test_non_str_raises_type_error(bad):
    with pytest.raises(TypeError):
        top_words(bad)
