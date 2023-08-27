from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.files import files
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_files(_ock_resolve: MagicMock):
    assert await files() == [
        "resources/binary_file",
        "resources/blame_1",
        "resources/blame_2",
        "resources/empty_file",
        "resources/not_exist",
    ]
