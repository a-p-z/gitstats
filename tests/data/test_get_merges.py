from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.shortlog import get_merges
from tests import a_shortlog


@mark.asyncio
@patch("gitstats.data.shortlog.get_authors_by_email")
@patch("gitstats.data.shortlog.shortlog_merges")
async def test_get_merges(mock_git_shortlog_merges: MagicMock, mock_get_authors_by_email: MagicMock):
    shortlog = a_shortlog()
    mock_git_shortlog_merges.return_value = [
        {
            "author-name": shortlog.author.name,
            "author-email": shortlog.author.email,
            "commits": shortlog.commits,
        }
    ]
    mock_get_authors_by_email.return_value = {shortlog.author.email: shortlog.author}
    merges = await get_merges()
    assert merges == [shortlog]
