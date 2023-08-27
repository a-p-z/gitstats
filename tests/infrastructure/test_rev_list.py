from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.infrastructure.git.rev_list import rev_list_no_merges_count_head
from tests import mock_scope_resolver


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_rev_list_no_merges_count_head(_mock_resolve: MagicMock):
    assert await rev_list_no_merges_count_head() == 42
