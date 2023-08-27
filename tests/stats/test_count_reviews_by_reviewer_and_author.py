from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.data.model.author import Author
from gitstats.data.model.author import Reviewer
from gitstats.stats.reviews import count_reviews_by_reviewer_and_author
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_count_reviews_by_reviewer_and_author(_mock_scope_resolve: MagicMock):
    assert await count_reviews_by_reviewer_and_author() == {
        Reviewer("Numa Pompilio", "numa.pompilio@gitstats.org"): {
            Author("Numa Pompilio", "numa.pompilio@gitstats.org"): 1,
            Author("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"): 1,
        },
        Reviewer("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org"): {
            Author("Numa Pompilio", "numa.pompilio@gitstats.org"): 1
        },
    }
