from unittest.mock import MagicMock
from unittest.mock import patch

from importlib_resources import files
from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.refs_remotes_origin import refs_remotes_origin
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_refs_remotes_origin(mock_resolve: MagicMock):
    mock_resolve.return_value.for_each_ref.return_value = (files("tests") / "resources" / "for_each_ref").read_text()

    assert await refs_remotes_origin() == [
        {
            "author-email": "romolo@gitstats.org",
            "author-name": "Romolo",
            "date": "2023-08-26 05:48:01 +0000",
            "name": "refs/remotes/origin/1625411301247414097",
        },
        {
            "author-email": "anco.marzio@gitstats.org",
            "author-name": "Anco Marzio",
            "date": "2023-08-27 05:12:00 +0000",
            "name": "refs/remotes/origin/7339099248855462398",
        },
    ]
