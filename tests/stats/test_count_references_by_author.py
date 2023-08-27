from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.model.author import Author
from gitstats.stats.references import count_references_by_author
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_count_references_by_author(_mock_resolve: MagicMock):
    assert await count_references_by_author() == {
        Author("Romolo", "romolo@gitstats.org"): 1,
        Author("unknown", "anco.marzio@gitstats.org"): 1,
    }
