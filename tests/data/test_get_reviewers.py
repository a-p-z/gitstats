from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.model.author import Reviewer
from gitstats.data.reviewers import get_reviewers
from tests import clear_cache
from tests import mock_scope_resolver
from tests import mock_scope_resolver_with_username_map


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_reviewers(_mock_resolve: MagicMock):
    reviewers = await get_reviewers()
    assert reviewers == [
        Reviewer("Numa Pompilio", "numa.pompilio@gitstats.org"),
        Reviewer("Romolo", "romolo@gitstats.org"),
        Reviewer("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    ]


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver_with_username_map)
async def test_get_reviewers_with_username_map(_mock_resolve: MagicMock):
    reviewers = await get_reviewers()
    assert reviewers == [
        Reviewer("Numa Pompilio", "numa.pompilio@gitstats.org"),
        Reviewer("Romolo", "romolo@gitstats.org"),
        Reviewer("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    ]
