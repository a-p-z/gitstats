from datetime import UTC
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.model.author import Author
from gitstats.data.model.ref import Ref
from gitstats.data.references import get_origin_remote_references
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_origin_remote_references(_mock_resolve: MagicMock):
    assert await get_origin_remote_references() == [
        Ref(
            name="refs/remotes/origin/1625411301247414097",
            author=Author("Romolo", "romolo@gitstats.org"),
            date=datetime(2023, 8, 26, 5, 48, 1, tzinfo=UTC),
        ),
        Ref(
            name="refs/remotes/origin/7339099248855462398",
            author=Author("unknown", "anco.marzio@gitstats.org"),
            date=datetime(2023, 8, 27, 5, 12, tzinfo=UTC),
        ),
    ]
