import pytest

from textstats import TextCounts, count_text


def test_counts_lines_words_characters():
    assert count_text("one two\nthree\n") == TextCounts(lines=2, words=3, characters=14)


def test_empty_text():
    assert count_text("") == TextCounts(lines=0, words=0, characters=0)


def test_last_line_without_newline_counts():
    assert count_text("a\nb").lines == 2


def test_apostrophes_stay_inside_words():
    assert count_text("don't stop").words == 2


def test_punctuation_is_not_a_word():
    assert count_text("hi --- there!").words == 2


def test_rejects_non_string():
    with pytest.raises(TypeError):
        count_text(None)
