from unittest.mock import MagicMock
from unittest.mock import patch

from importlib_resources import files
from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.usernames import get_usernames_by_email
from gitstats.infrastructure.git.usernames import get_users
from tests import clear_cache
from tests import mock_scope_resolver
from tests import mock_scope_resolver_with_username_map


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_usernames_by_email_without_username_map(_mock_resolve: MagicMock):
    assert await get_usernames_by_email() == {}


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver_with_username_map)
async def test_get_usernames_by_email_with_username_map(_mock_resolve: MagicMock):
    assert await get_usernames_by_email() == {
        "tarquinio.il.superbo.@gitstats.org": "Tarquinio il Superbo",
        "numa.pompilio@gitstats.org": "Numa Pompilio",
        "romolo1@gitstats.org": "Romolo",
        "romolo@gitstats.org": "Romolo",
    }


@mark.asyncio
@mark.parametrize(
    "username_map", (None, str(files("tests") / "resources"), str(files("tests") / "resources" / "not-exist"))
)
async def test_get_users_without_username_map(username_map: str):
    assert await get_users(username_map) == []


@mark.asyncio
async def test_get_users():
    assert await get_users(str(files("tests") / "resources" / "username_map")) == [
        {"email": "numa.pompilio@gitstats.org", "username": "Numa Pompilio"},
        {"email": "romolo1@gitstats.org", "username": "Romolo"},
        {"email": "romolo@gitstats.org", "username": "Romolo"},
        {"email": "tarquinio.il.superbo.@gitstats.org", "username": "Tarquinio il Superbo"},
    ]
