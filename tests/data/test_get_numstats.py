from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.data.model.numstat import Numstat
from gitstats.data.numstats import get_numstats
from tests import a_diffstat
from tests import a_log


@mark.asyncio
@patch("gitstats.data.numstats.get_logs")
async def test_get_numstats(mock_get_logs: MagicMock):
    diffstat1 = a_diffstat()
    diffstat2 = a_diffstat()
    log1 = a_log()
    log2 = a_log(diffstats=[diffstat1, diffstat2])
    mock_get_logs.return_value = [log1, log2]
    numstats = await get_numstats()
    assert numstats == [
        Numstat(log1.hash, log1.parent, log1.date, log1.subject, log1.author, log1.committer),
        Numstat(
            log2.hash,
            log2.parent,
            log2.date,
            log2.subject,
            log2.author,
            log2.committer,
            diffstat1.file,
            diffstat1.insertions,
            diffstat1.deletions,
        ),
        Numstat(
            log2.hash,
            log2.parent,
            log2.date,
            log2.subject,
            log2.author,
            log2.committer,
            diffstat2.file,
            diffstat2.insertions,
            diffstat2.deletions,
        ),
    ]
