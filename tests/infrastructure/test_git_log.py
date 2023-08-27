from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.log import log
from gitstats.infrastructure.git.log import log_numstat
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_log(_mock_resolve: MagicMock):
    assert await log() == [
        {
            "author-date": "2023-08-26T07:35:09+00:00",
            "author-email": "numa.pompilio@gitstats.org",
            "author-name": "numa.pompilio",
            "committer-email": "romolo1@gitstats.org",
            "committer-name": "Romolo",
            "committer-date": "2023-08-26T07:35:09+00:00",
            "hash": "5504c8b70e55a0a55e2d5a8913eb3c2b9eb06e77",
            "parent": "",
            "subject": "subject Approved by Numa Pompilio, Tarquinio il Superbo",
        },
        {
            "author-date": "2023-08-26T16:34:21+00:00",
            "author-email": "romolo@gitstats.org",
            "author-name": "Romolo",
            "committer-email": "numa.pompilio@gitstats.org",
            "committer-name": "Numa Pompilio",
            "committer-date": "2023-08-26T16:34:21+00:00",
            "hash": "aa42d35efcd2b5f6f537625547824be26576a3ff",
            "parent": "5504c8b70e55a0a55e2d5a8913eb3c2b9eb06e77",
            "subject": "subject ~tarqsup",
        },
        {
            "author-date": "2023-08-26T03:20:53+00:00",
            "author-email": "tarquinio.il.superbo.@gitstats.org",
            "author-name": "Tarquinio il Superbo",
            "committer-email": "numa.pompilio@GITstats.org",
            "committer-name": "numa.pompilio",
            "committer-date": "2023-08-26T03:20:53+00:00",
            "hash": "2be6495b2cfb4dbaffe09db6e5889b6642ebf782",
            "parent": "aa42d35efcd2b5f6f537625547824be26576a3ff",
            "subject": "subject reviewed by numa.pompilio",
        },
        {
            "author-date": "2023-08-26T03:31:14+00:00",
            "author-email": "numa.pompilio@gitstats.org",
            "author-name": "Numa Pompilio",
            "committer-email": "tarquinio.il.superbo.@gitstats.org",
            "committer-name": "Tarquinio il Superbo",
            "committer-date": "2023-08-26T03:31:14+00:00",
            "hash": "c91053f72606babac33fa9a301373b8e4dc5e93e",
            "parent": "2be6495b2cfb4dbaffe09db6e5889b6642ebf782",
            "subject": "subject 7307067630998898480",
        },
    ]


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_log_numstat(_mock_resolve: MagicMock):
    assert await log_numstat() == [
        {
            "deletions": 77,
            "filename": "log_numstat_1",
            "hash": "45453791a689235cc3af3ee53ad09840cfb77d38",
            "insertions": 33,
        },
        {
            "deletions": 0,
            "filename": "log_numstat_2",
            "hash": "45453791a689235cc3af3ee53ad09840cfb77d38",
            "insertions": 34,
        },
        {
            "deletions": 1,
            "filename": "log_numstat_2",
            "hash": "a03660e8f78cda8f8599b4ed3da46b8ce50e592b",
            "insertions": 2,
        },
        {
            "deletions": 0,
            "filename": "log_numstat_1",
            "hash": "a03660e8f78cda8f8599b4ed3da46b8ce50e592b",
            "insertions": 1,
        },
        {
            "deletions": 0,
            "filename": "log_numstat_3",
            "hash": "a03660e8f78cda8f8599b4ed3da46b8ce50e592b",
            "insertions": 0,
        },
    ]
