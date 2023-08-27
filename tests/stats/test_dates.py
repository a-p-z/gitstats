from datetime import UTC
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.stats.dates import get_last_update
from gitstats.stats.dates import get_start_date
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_start_date(_mock_resolve: MagicMock):
    assert await get_start_date() == datetime(2023, 8, 26, 3, 20, 53, tzinfo=UTC)


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_get_last_update(_mock_resolve: MagicMock):
    assert await get_last_update() == datetime(2023, 8, 26, 16, 34, 21, tzinfo=UTC)
