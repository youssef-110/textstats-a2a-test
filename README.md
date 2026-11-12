# textstats

A tiny Python library and command line tool that reports statistics about a
text file: lines, words, characters and the most frequent words. Standard
library only.

```bash
python -m textstats notes.txt --top 3
```

```text
lines:      2
words:      13
characters: 63
top words:
     2  café
     1  don't
     1  end
```

Options: `--top N` (default 5, 0 hides the list), `--keep-stopwords`, and `-`
as the file to read standard input.

```python
from textstats import count_text
from textstats.frequency import top_words

count_text("one two\nthree")        # TextCounts(lines=2, words=3, characters=13)
top_words("the cat and the hat", 2)  # [('cat', 1), ('hat', 1)]
```

Tests: `python -m pytest`

## How this was built

This project is a test of agent-to-agent messaging over a NetBird network. Two
AI agents on two different computers built it by exchanging messages directly
between the machines, with no person relaying anything:

| Part | Who |
| --- | --- |
| Project plan, split of work, repository | Youssef's agent (coordinator, Windows) |
| `textstats/core.py`, `textstats/cli.py`, their tests | Youssef's agent |
| `textstats/frequency.py`, `tests/test_frequency.py` | Alan's agent (Linux), sent as a reply |
| Code review of the coordinator's part | Alan's agent: 7 findings, 3 of them real bugs |
| Fixes from the review, shared `textstats/words.py`, consistency test | Youssef's agent |

Alan's agent answered automatically each time: it was only listening, started
a model run when a request arrived, and replied in about 17 seconds.
