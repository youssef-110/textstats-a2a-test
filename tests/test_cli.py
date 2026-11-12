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


def test_non_utf8_file_is_an_error_not_a_traceback(tmp_path, capsys):
    sample = tmp_path / "latin1.txt"
    sample.write_bytes("caf\xe9".encode("latin-1"))

    assert main([str(sample)]) == 1
    assert "not UTF-8" in capsys.readouterr().err


def test_negative_top_is_rejected(tmp_path, capsys):
    import pytest

    sample = tmp_path / "sample.txt"
    sample.write_text("cat", encoding="utf-8")
    with pytest.raises(SystemExit) as stop:
        main([str(sample), "--top", "-3"])
    assert stop.value.code == 2
    assert "must be 0 or more" in capsys.readouterr().err


def test_reads_standard_input(monkeypatch, capsys):
    import io

    monkeypatch.setattr("sys.stdin", io.StringIO("cat cat dog"))
    assert main(["-"]) == 0
    out = capsys.readouterr().out
    assert "words:      3" in out
    assert "2  cat" in out
