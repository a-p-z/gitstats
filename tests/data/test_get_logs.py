from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.logs import get_logs
from tests import a_diffstat
from tests import a_log


@mark.asyncio
@patch("gitstats.data.logs.get_committers_by_email")
@patch("gitstats.data.logs.get_authors_by_email")
@patch("gitstats.data.logs.log")
@patch("gitstats.data.logs.log_numstat")
async def test_get_logs(
    mock_git_log_numstat: MagicMock,
    mock_git_log: MagicMock,
    mock_get_authors_by_email: MagicMock,
    mock_get_committers_by_email: MagicMock,
):
    diffstat1 = a_diffstat()
    diffstat2 = a_diffstat(diffstat1.hash)
    log = a_log(diffstat1.hash, diffstats=[diffstat1, diffstat2])
    mock_git_log_numstat.return_value = [
        {
            "hash": diffstat1.hash,
            "filename": str(diffstat1.file),
            "insertions": diffstat1.insertions,
            "deletions": diffstat1.deletions,
        },
        {
            "hash": diffstat2.hash,
            "filename": str(diffstat2.file),
            "insertions": diffstat2.insertions,
            "deletions": diffstat2.deletions,
        },
    ]
    mock_git_log.return_value = [
        {
            "hash": log.hash,
            "parent": log.parent,
            "author-date": log.date.isoformat(),
            "author-email": log.author.email,
            "committer-email": log.committer.email,
            "subject": log.subject,
            "diffstats": [
                {
                    "filename": diffstat1.file,
                    "insertions": diffstat1.insertions,
                    "deletions": diffstat1.deletions,
                },
                {
                    "filename": diffstat2.file,
                    "insertions": diffstat2.insertions,
                    "deletions": diffstat2.deletions,
                },
            ],
        }
    ]
    mock_get_authors_by_email.return_value = {log.author.email: log.author}
    mock_get_committers_by_email.return_value = {log.committer.email: log.committer}
    logs = await get_logs()
    assert logs == [log]
