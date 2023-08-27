from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.shortlog import shortlog_merges
from gitstats.infrastructure.git.shortlog import shortlog_no_merges
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_shortlog_no_merges(_mock_resolve: MagicMock):
    assert await shortlog_no_merges() == [
        {"author-name": "Tullo Ostilio", "author-email": "tullo.ostilio@gitstats.org", "commits": 42},
        {"author-name": "Servio Tullio", "author-email": "servio.tullio@gitstats.org", "commits": 12},
    ]


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_shortlog_merges(_mock_resolve: MagicMock):
    assert await shortlog_merges() == [
        {"author-name": "Tullo Ostilio", "author-email": "tullo.ostilio@gitstats.org", "commits": 42},
        {"author-name": "Servio Tullio", "author-email": "servio.tullio@gitstats.org", "commits": 12},
    ]
