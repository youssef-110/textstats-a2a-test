from textstats.cli import main


def test_reports_counts_and_top_words(tmp_path, capsys):
    sample = tmp_path / "sample.txt"
    sample.write_text("the cat sat\nthe cat ran\n", encoding="utf-8")

    assert main([str(sample), "--top", "1"]) == 0

    out = capsys.readouterr().out
    assert "lines:      2" in out
    assert "words:      6" in out
    assert "characters: 24" in out
    assert "2  cat" in out
    assert "the" not in out.split("top words:")[1], "stopwords are hidden by default"


def test_keep_stopwords_shows_them(tmp_path, capsys):
    sample = tmp_path / "sample.txt"
    sample.write_text("the the the cat", encoding="utf-8")

    assert main([str(sample), "--top", "1", "--keep-stopwords"]) == 0
    assert "3  the" in capsys.readouterr().out


def test_top_zero_hides_the_list(tmp_path, capsys):
    sample = tmp_path / "sample.txt"
    sample.write_text("cat cat", encoding="utf-8")

    assert main([str(sample), "--top", "0"]) == 0
    assert "top words" not in capsys.readouterr().out


def test_missing_file_is_an_error(tmp_path, capsys):
    assert main([str(tmp_path / "nope.txt")]) == 1
    assert "textstats:" in capsys.readouterr().err
