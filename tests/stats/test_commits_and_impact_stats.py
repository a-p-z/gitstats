from datetime import UTC
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.stats.commits_and_impact import count_commits
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_author
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_extension
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_file
from gitstats.stats.commits_and_impact import count_commits_and_impact_over_time
from gitstats.stats.commits_and_impact import count_commits_and_impact_over_time_by_author
from gitstats.stats.commits_and_impact import count_merges
from gitstats.stats.commits_and_impact import cumulate_commits_and_impact_over_time_by_author
from gitstats.stats.model.commits_and_impact import CommitsAndImpact
from tests import a_blame
from tests import a_diffstat
from tests import a_file
from tests import a_hash
from tests import a_log
from tests import a_numstat
from tests import a_shortlog
from tests import an_author
from tests import another_author


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_commits")
async def test_count_commits(mock_get_commits: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    log1, log2, log3 = (
        a_shortlog(author2, 1),
        a_shortlog(author1, 1),
        a_shortlog(author2, 1),
    )
    mock_get_commits.return_value = [log1, log2, log3]
    assert await count_commits() == {author1: 1, author2: 2}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_merges")
async def test_count_merges(mock_get_merges: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    log1, log2, log3 = (
        a_shortlog(author2, 1),
        a_shortlog(author1, 1),
        a_shortlog(author2, 1),
    )
    mock_get_merges.return_value = [log1, log2, log3]
    assert await count_merges() == {author1: 1, author2: 2}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_blames")
@patch("gitstats.stats.commits_and_impact.get_logs")
@patch("gitstats.stats.commits_and_impact.get_numstats")
async def test_count_commits_and_impact_by_author(
    mock_get_numstats: MagicMock, mock_get_logs: MagicMock, mock_get_blames: MagicMock
):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_numstats.return_value = [
        a_numstat(author=author1, insertions=59, deletions=32),
        a_numstat(parent=f"{a_hash()} {a_hash()}", author=author1),
        a_numstat(author=author1, insertions=15, deletions=10),
        a_numstat(parent=f"{a_hash()} {a_hash()}", author=author1),
        a_numstat(author=author1, insertions=26, deletions=5),
        a_numstat(parent=f"{a_hash()} {a_hash()}", author=author1),
        a_numstat(author=author1, insertions=15, deletions=15),
        a_numstat(author=author2, insertions=3, deletions=4),
        a_numstat(parent=f"{a_hash()} {a_hash()}", author=author2),
        a_numstat(author=author2, insertions=33, deletions=7),
        a_numstat(parent=f"{a_hash()} {a_hash()}", author=author2),
        a_numstat(author=author2, insertions=17, deletions=2),
    ]

    mock_get_logs.return_value = [
        a_log(
            diffstats=[
                a_diffstat(insertions=32, deletions=22),
                a_diffstat(insertions=27, deletions=10),
            ]
        ),
        a_log(parent=f"{a_hash()} {a_hash()}"),
        a_log(diffstats=[a_diffstat(insertions=15, deletions=10)]),
        a_log(parent=f"{a_hash()} {a_hash()}"),
        a_log(diffstats=[a_diffstat(insertions=26, deletions=5)]),
        a_log(parent=f"{a_hash()} {a_hash()}"),
        a_log(diffstats=[a_diffstat(insertions=15, deletions=15)]),
        a_log(diffstats=[a_diffstat(insertions=3, deletions=4)]),
        a_log(parent=f"{a_hash()} {a_hash()}"),
        a_log(
            diffstats=[
                a_diffstat(insertions=20, deletions=6),
                a_diffstat(insertions=13, deletions=1),
            ]
        ),
        a_log(parent=f"{a_hash()} {a_hash()}"),
        a_log(diffstats=[a_diffstat(insertions=17, deletions=2)]),
    ]

    mock_get_blames.return_value = [
        a_blame(author=author1),
        a_blame(author=author1),
        a_blame(author=author1),
        a_blame(author=author2),
        a_blame(author=author2),
    ]

    assert await count_commits_and_impact_by_author() == {
        author1: CommitsAndImpact(4, 115, 62, 3, 243, 3),
        author2: CommitsAndImpact(3, 53, 13, 2, 243, 2),
    }


@mark.asyncio
async def test_cumulate_commits_and_impact_over_time_by_author_with_start_lt_end():
    start = datetime.now(tz=UTC)
    end = datetime.now(tz=UTC) - timedelta(days=1)
    cumulated = await cumulate_commits_and_impact_over_time_by_author(start, end, "1m", {})
    assert cumulated == {}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_authors")
@patch("gitstats.stats.commits_and_impact.get_logs")
async def test_cumulate_commits_and_impact_over_time_by_author(mock_get_logs: MagicMock, mock_authors: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_logs.return_value = [
        a_log(author=author1, date_="2022-10-03T20:58:23.134503+00:00"),
        a_log(author=author2, date_="2022-12-13T20:58:23.134503+00:00"),
    ]
    mock_authors.return_value = [author1, author2]
    start = datetime.fromisoformat("2022-10-03T20:58:23.134503+00:00")
    end = datetime.fromisoformat("2022-12-23T20:58:23.134503+00:00")
    heritage = {author2: CommitsAndImpact(1, 2, 3, 4, 5, 6)}
    cumulated = await cumulate_commits_and_impact_over_time_by_author(start, end, "1m", heritage)
    assert cumulated == {
        "2022-10": {
            author1: CommitsAndImpact(1, 0, 0),
            author2: CommitsAndImpact(1, 2, 3, 4, 5, 6),
        },
        "2022-11": {
            author1: CommitsAndImpact(1, 0, 0),
            author2: CommitsAndImpact(1, 2, 3, 4, 5, 6),
        },
        "2022-12": {
            author1: CommitsAndImpact(1, 0, 0),
            author2: CommitsAndImpact(2, 2, 3, 4, 5, 6),
        },
    }


@mark.asyncio
async def test_count_commits_and_impact_over_time_by_author_with_start_lt_end():
    start = datetime.now(tz=UTC)
    end = datetime.now(tz=UTC) - timedelta(days=1)
    count = await count_commits_and_impact_over_time_by_author(start, end, "1m")
    assert count == {}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_logs")
async def test_count_commits_and_impact_over_time(
    mock_get_logs: MagicMock,
):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_logs.return_value = [
        a_log(author=author1, date_="2022-10-03T20:58:23.134503+00:00"),
        a_log(author=author2, date_="2022-12-13T20:58:23.134503+00:00"),
    ]
    start = datetime.fromisoformat("2022-10-03T20:58:23.134503+00:00")
    end = datetime.fromisoformat("2022-12-23T20:58:23.134503+00:00")
    count = await count_commits_and_impact_over_time(start, end, "1m")
    assert count == {
        "2022-10": CommitsAndImpact(1, 0, 0),
        "2022-11": CommitsAndImpact(0, 0, 0),
        "2022-12": CommitsAndImpact(1, 0, 0),
    }


@mark.asyncio
async def test_count_commits_and_impact_over_time_with_start_lt_end():
    start = datetime.now(tz=UTC)
    end = datetime.now(tz=UTC) - timedelta(days=1)
    count = await count_commits_and_impact_over_time(start, end, "1m")
    assert count == {}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_logs")
async def test_count_commits_and_impact_over_time_by_author(mock_get_logs: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_logs.return_value = [
        a_log(author=author1, date_="2022-10-03T20:58:23.134503+00:00"),
        a_log(author=author2, date_="2022-12-13T20:58:23.134503+00:00"),
    ]
    start = datetime.fromisoformat("2022-10-03T20:58:23.134503+00:00")
    end = datetime.fromisoformat("2022-12-23T20:58:23.134503+00:00")
    count = await count_commits_and_impact_over_time_by_author(start, end, "1m")
    assert count == {
        "2022-10": {author1: CommitsAndImpact(1, 0, 0)},
        "2022-11": {},
        "2022-12": {author2: CommitsAndImpact(1, 0, 0)},
    }


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_logs")
async def test_count_commits_and_impact_over_time_by_author_1d(mock_get_logs: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_logs.return_value = [
        a_log(author=author1, date_="2022-12-10T20:58:23.134503+00:00"),
        a_log(author=author2, date_="2022-12-13T20:58:23.134503+00:00"),
    ]
    start = datetime.fromisoformat("2022-12-10T20:58:23.134503+00:00")
    end = datetime.fromisoformat("2022-12-13T20:58:23.134503+00:00")
    count = await count_commits_and_impact_over_time_by_author(start, end, "1d")
    assert count == {
        "2022-12-10": {author1: CommitsAndImpact(1, 0, 0)},
        "2022-12-11": {},
        "2022-12-12": {},
        "2022-12-13": {author2: CommitsAndImpact(1, 0, 0)},
    }


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_logs")
async def test_count_commits_and_impact_over_time_by_author_1y(mock_get_logs: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    mock_get_logs.return_value = [
        a_log(author=author1, date_="2022-10-03T20:58:23.134503+00:00"),
        a_log(author=author2, date_="2022-12-13T20:58:23.134503+00:00"),
    ]
    start = datetime.fromisoformat("2022-10-03T20:58:23.134503+00:00")
    end = datetime.fromisoformat("2022-12-23T20:58:23.134503+00:00")
    count = await count_commits_and_impact_over_time_by_author(start, end, "1y")
    assert count == {"2022": {author1: CommitsAndImpact(1, 0, 0), author2: CommitsAndImpact(1, 0, 0)}}


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_numstats")
async def test_count_commits_and_impact_by_file(mock_get_numstats: MagicMock):
    file1, file2 = a_file(), a_file()
    mock_get_numstats.return_value = [
        a_numstat(filename=file1, insertions=4, deletions=4),
        a_numstat(filename=file1, insertions=5, deletions=2),
        a_numstat(filename=file1, insertions=6, deletions=1),
        a_numstat(filename=file2, insertions=11, deletions=4),
        a_numstat(filename=file2, insertions=8, deletions=7),
    ]

    assert await count_commits_and_impact_by_file() == {
        file1: CommitsAndImpact(3, 15, 7),
        file2: CommitsAndImpact(2, 19, 11),
    }


@mark.asyncio
@patch("gitstats.stats.commits_and_impact.get_numstats")
async def test_count_commits_and_impact_by_extension(mock_get_numstats: MagicMock):
    file1, file2 = a_file("java"), a_file("py")
    mock_get_numstats.return_value = [
        a_numstat(filename=file1, insertions=4, deletions=4),
        a_numstat(filename=file1, insertions=5, deletions=2),
        a_numstat(filename=file1, insertions=6, deletions=1),
        a_numstat(filename=file2, insertions=11, deletions=4),
        a_numstat(filename=file2, insertions=8, deletions=7),
    ]

    assert await count_commits_and_impact_by_extension() == {
        ".java": CommitsAndImpact(3, 15, 7),
        ".py": CommitsAndImpact(2, 19, 11),
    }
