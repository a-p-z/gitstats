from datetime import UTC
from datetime import datetime
from datetime import timedelta

from gitstats.data.model.author import Author
from tests import an_author


def test_is_dead():
    assert an_author(end=datetime.now(tz=UTC) - timedelta(366)).is_dead()


def test_is_not_dead():
    assert not an_author(end=datetime.now(tz=UTC) - timedelta(365)).is_dead()


def test_repr():
    author = an_author()
    assert str(author) == author.name


def test_eq():
    author = an_author()
    assert author == author


def test_not_eq():
    assert an_author() != "string"


def test_ordering():
    author1 = Author(
        "Romolo",
        "romolo@gitstats.org",
        datetime.now(tz=UTC),
        datetime.now(tz=UTC),
        "romolo",
    )
    author2 = Author(
        "Servio Tullio",
        "servio.tullio@gitstats.org",
        datetime.now(tz=UTC),
        datetime.now(tz=UTC),
        "tullser",
    )
    assert sorted([author2, author1]) == [author1, author2]
