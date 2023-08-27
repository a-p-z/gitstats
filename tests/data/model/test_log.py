from datetime import UTC
from datetime import datetime

from gitstats.data.model.diffstat import Diffstat
from gitstats.data.model.log import Log
from tests import a_file
from tests import a_hash
from tests import a_subject
from tests import an_author


def test_is_merge():
    log = Log(
        a_hash(),
        f"{a_hash()} {a_hash()}",
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        [],
    )
    assert log.is_merge()


def test_is_not_merge():
    log = Log(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        [],
    )
    assert not log.is_merge()


def test_is_commit():
    log = Log(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        [],
    )
    assert log.is_commit()


def test_is_not_commit():
    log = Log(
        a_hash(),
        f"{a_hash()} {a_hash()}",
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        [],
    )
    assert not log.is_commit()


def test_insertions():
    diffstats = [Diffstat(a_hash(), a_file(), 9, 0), Diffstat(a_hash(), a_file(), 33, 0)]
    log = Log(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        diffstats,
    )
    assert log.insertions == 42


def test_deletions():
    diffstats = [Diffstat(a_hash(), a_file(), 0, 9), Diffstat(a_hash(), a_file(), 0, 33)]
    log = Log(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        diffstats,
    )
    assert log.deletions == 42


def test_impact():
    diffstats = [Diffstat(a_hash(), a_file(), 14, 7), Diffstat(a_hash(), a_file(), 7, 14)]
    log = Log(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
        diffstats,
    )
    assert log.impact == 42
