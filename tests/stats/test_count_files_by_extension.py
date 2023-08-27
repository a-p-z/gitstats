from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.model.file import File
from gitstats.stats.extensions import count_files_by_extension


@mark.asyncio
@patch("gitstats.stats.extensions.get_files")
async def test_count_files_by_extension(mock_get_files: MagicMock):
    mock_get_files.return_value = [
        File("test/stats/test_extension_commits.py"),
        File("stats/extensions.py"),
        File("requirements.txt"),
    ]

    assert await count_files_by_extension() == {".py": 2, ".txt": 1}
