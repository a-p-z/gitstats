from datetime import UTC
from datetime import datetime

import pytest

from gitstats.data.model.numstat import Numstat
from tests import a_file
from tests import a_hash
from tests import a_subject
from tests import an_author


@pytest.mark.parametrize("insertions, deletions, impact", [[0, 0, 0], [9, 33, 42]])
def test_impact(insertions: int, deletions: int, impact: int):
    date = datetime.now(tz=UTC)
    numstat = Numstat(
        a_hash(),
        a_hash(),
        date,
        a_subject(),
        an_author(),
        an_author(),
        a_file(),
        insertions,
        deletions,
    )
    assert numstat.impact == impact


def test_is_merge():
    parent = f"{a_hash()} {a_hash()}"
    numstat = Numstat(
        a_hash(),
        parent,
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
    )
    assert numstat.is_merge()


def test_is_not_merge():
    numstat = Numstat(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
    )
    assert not numstat.is_merge()


def test_is_commit():
    numstat = Numstat(
        a_hash(),
        a_hash(),
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
    )
    assert numstat.is_commit()


def test_is_not_commit():
    numstat = Numstat(
        a_hash(),
        f"{a_hash()} {a_hash()}",
        datetime.now(tz=UTC),
        a_subject(),
        an_author(),
        an_author(),
    )
    assert not numstat.is_commit()
