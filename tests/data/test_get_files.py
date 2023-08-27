from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.files import get_files
from tests import a_file


@mark.asyncio
@patch("gitstats.data.files.files")
async def test_get_files(mock_git_ls_files: MagicMock):
    file = a_file()
    mock_git_ls_files.return_value = [file]
    files = await get_files()
    assert files == [file]
