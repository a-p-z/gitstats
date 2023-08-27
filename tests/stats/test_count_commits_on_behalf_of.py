from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark

from gitstats.stats.commits_on_behalf_of import count_commits_on_behalf_of
from tests import a_diffstat
from tests import a_hash
from tests import a_log
from tests import an_author
from tests import another_author


@mark.asyncio
@patch("gitstats.stats.commits_on_behalf_of.get_logs")
async def test_count_commits_on_behalf_of(mock_get_logs: MagicMock):
    author1 = an_author()
    author2 = another_author(author1)
    author3 = another_author(author1, author2)
    mock_get_logs.return_value = [
        a_log(parent=f"{a_hash()} {a_hash()}", author=author1, committer=author1),
        a_log(parent=f"{a_hash()} {a_hash()}", author=author2, committer=author1),
        a_log(author=author1, committer=author2, diffstats=[a_diffstat()]),
        a_log(parent=f"{a_hash()} {a_hash()}", author=author1, committer=author2),
        a_log(author=author2, committer=author2, diffstats=[a_diffstat()]),
        a_log(parent=f"{a_hash()} {a_hash()}", author=author3, committer=author3),
        a_log(author=author3, committer=author3, diffstats=[a_diffstat()]),
    ]

    assert await count_commits_on_behalf_of() == {
        author1: {author1: 1, author2: 1},
        author2: {author1: 2, author2: 1},
        author3: {author3: 2},
    }
