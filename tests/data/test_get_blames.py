from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.blames import get_blames
from tests import a_blame


@mark.asyncio
@patch("gitstats.data.blames.get_committers_by_email")
@patch("gitstats.data.blames.get_authors_by_email")
@patch("gitstats.data.blames.blame")
async def test_get_blames(
    mock_git_blame: MagicMock,
    mock_get_authors_by_email: MagicMock,
    mock_get_committers_by_email: MagicMock,
):
    blame = a_blame()
    mock_git_blame.return_value = [
        {
            "hash": blame.hash,
            "author": blame.author.name,
            "author-mail": blame.author.email,
            "committer": blame.committer.name,
            "committer-mail": blame.committer.email,
            "summary": blame.summary,
            "filename": blame.file.name,
            "content": blame.content,
        }
    ]
    mock_get_authors_by_email.return_value = {blame.author.email: blame.author}
    mock_get_committers_by_email.return_value = {blame.committer.email: blame.committer}
    blames = await get_blames()
    assert blames == [blame]
