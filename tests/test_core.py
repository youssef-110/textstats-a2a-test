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


def test_lone_apostrophes_are_not_words():
    assert count_text("' '' - '").words == 0


def test_quoted_word_is_one_word():
    assert count_text("'quoted'").words == 1


def test_non_ascii_words_stay_whole():
    assert count_text("café naïve привет").words == 3


def test_unicode_line_separator_counts_as_a_line_break():
    assert count_text("a b").lines == 2
