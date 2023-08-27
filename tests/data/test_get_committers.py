from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.committers import get_committers_by_email
from gitstats.data.model.author import Author
from gitstats.data.model.author import Committer
from tests import clear_cache
from tests import mock_scope_resolver
from tests import mock_scope_resolver_with_username_map


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_committers_by_email(_mock_resolve: MagicMock):
    committers = await get_committers_by_email()
    assert committers == {
        "romolo1@gitstats.org": Committer("Romolo", "romolo1@gitstats.org"),
        "numa.pompilio@gitstats.org": Committer("numa.pompilio", "numa.pompilio@gitstats.org"),
        "tarquinio.il.superbo.@gitstats.org": Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    }


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver_with_username_map)
async def test_get_committers_by_email_with_username_map(_mock_resolve: MagicMock):
    committers = await get_committers_by_email()
    assert committers == {
        "romolo1@gitstats.org": Committer("Romolo", "romolo1@gitstats.org"),
        "numa.pompilio@gitstats.org": Committer("numa.pompilio", "numa.pompilio@gitstats.org"),
        "tarquinio.il.superbo.@gitstats.org": Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"),
    }
