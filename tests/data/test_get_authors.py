from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.authors import get_authors
from gitstats.data.authors import get_authors_by_email
from gitstats.data.model.author import Author
from tests import clear_cache
from tests import mock_scope_resolver
from tests import mock_scope_resolver_with_username_map


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_authors_without_username_map(_mock_resolve: MagicMock):
    authors = await get_authors()
    assert authors == [
        Author("Numa Pompilio", "numa.pompilio@gitstats.org"),
        Author("Romolo", "romolo@gitstats.org"),
        Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    ]


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver_with_username_map)
async def test_get_authors_with_username_map(_mock_resolve: MagicMock):
    authors = await get_authors()
    assert authors == [
        Author("Numa Pompilio", "numa.pompilio@gitstats.org"),
        Author("Romolo", "romolo@gitstats.org"),
        Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    ]


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_authors_by_email(_mock_resolve: MagicMock):
    authors = await get_authors_by_email()
    assert authors == {
        "numa.pompilio@gitstats.org": Author("Numa Pompilio", "numa.pompilio@gitstats.org"),
        "romolo@gitstats.org": Author("Romolo", "romolo@gitstats.org"),
        "tarquinio.il.superbo.@gitstats.org": Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    }


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver_with_username_map)
async def test_get_authors_by_email_with_username_map(_mock_resolve: MagicMock):
    authors = await get_authors_by_email()
    assert authors == {
        "numa.pompilio@gitstats.org": Author("Numa Pompilio", "numa.pompilio@gitstats.org"),
        "romolo@gitstats.org": Author("Romolo", "romolo@gitstats.org"),
        "tarquinio.il.superbo.@gitstats.org": Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    }
