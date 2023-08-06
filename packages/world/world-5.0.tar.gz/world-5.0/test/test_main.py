import sys
import world

from world.__main__ import main

import pytest


def argv(*args):
    args = list(args)
    args.insert(0, 'argv0')
    return args


def test_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(('--version',))
    assert exc_info.value.code == 0
    out, err = capsys.readouterr()
    assert out.strip() == f'world {world.__version__}'


def test_main(capsys):
    code = main(('de',))
    assert code == 0
    out, err = capsys.readouterr()
    assert out.strip() == 'de originates from Germany'


def test_main_unknown_code(capsys):
    code = main(('xx',))
    assert code == 1
    out, err = capsys.readouterr()
    assert out.strip() == 'Where in the world is xx?'


def test_main_unknown_codes(capsys):
    code = main(('xx', 'yy'))
    assert code == 2
    out, err = capsys.readouterr()
    assert out == """\
Where in the world is xx?
Where in the world is yy?
"""


def test_reverse(capsys):
    code = main(('-r', 'Germany'))
    assert code == 0
    out, err = capsys.readouterr()
    assert out == """\
Matches for "Germany":
  de    : Germany
"""


def test_multiple_reverse_matches(capsys):
    code = main(('-r', 'united'))
    assert code == 0
    out, err = capsys.readouterr()
    assert out == """\
Matches for "united":
  ae    : United Arab Emirates (the)
  gb    : United Kingdom of Great Britain and Northern Ireland (the)
  tz    : Tanzania, United Republic of
  uk    : United Kingdom (common practice)
  um    : United States Minor Outlying Islands (the)
  us    : United States of America (the)
"""


def test_no_reverse_match(capsys):
    code = main(('-r', 'freedonia'))
    assert code == 1
    out, err = capsys.readouterr()
    assert out.strip() == 'Where in the world is freedonia?'


def test_multiple_reverse_searches(capsys):
    code = main(('-r', 'canada', 'mexico'))
    assert code == 0
    out, err = capsys.readouterr()
    assert out == """\
Matches for "canada":
  ca    : Canada

Matches for "mexico":
  mx    : Mexico
"""


def test_all(capsys):
    code = main(('--all',))
    assert code == 0
    out, err = capsys.readouterr()
    # Rather than test the entire output, just test the first and last.
    output = out.splitlines()
    assert output[1].strip() == 'ad: Andorra'
    assert output[-1].strip() == 'zw    : Zimbabwe'


def test_no_domains(capsys):
    code = main(())
    assert code == 0
    out, err = capsys.readouterr()
    output = out.splitlines()
    # The repeated domain argument gets printed differently in Python 3.8 vs
    # all later Python versions.
    extra = '...' if sys.version_info >= (3, 9) else '[domain ...]'
    assert output[0].strip() == f'usage: world [-h] [--version] [-r] [-a] [domain {extra}]'
