from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture
from pytest import mark

from gitstats.infrastructure.git.blame import blame
from tests import clear_cache
from tests import mock_scope_resolver


@fixture(autouse=True)
def before_each():
    clear_cache()


@mark.asyncio
@patch("gitstats.infrastructure.git.log.application_scope.resolve", side_effect=mock_scope_resolver)
async def test_git_blame(_mock_resolve: MagicMock):
    assert sorted(await blame(), key=lambda x: x["author-time"]) == [
        {
            "author": "Numa Pompilio",
            "author-mail": "<numa.pompilio@gitstats.org>",
            "author-time": "1664823231",
            "author-tz": "+0200",
            "committer": "Tullo Ostilio",
            "committer-mail": "<tullo.ostilio@gitstats.org>",
            "committer-time": "1692613007",
            "committer-tz": "+0300",
            "content": "        content 1",
            "filename": "blame_1",
            "hash": "b9e10cf0fa1eb7245a66a8e497375aecf9e85eec",
            "summary": "summary 1",
        },
        {
            "author": "Numa Pompilio",
            "author-mail": "<numa.pompilio@gitstats.org>",
            "author-time": "1664823232",
            "author-tz": "+0200",
            "committer": "Tullo Ostilio",
            "committer-mail": "<tullo.ostilio@gitstats.org>",
            "committer-time": "1692613007",
            "committer-tz": "+0300",
            "content": "        content 2",
            "filename": "blame_1",
            "hash": "b9e10cf0fa1eb7245a66a8e497375aecf9e85eec",
            "summary": "summary 2",
        },
        {
            "author": "Tarquinio Prisco",
            "author-mail": "<tarquinio.prisco@gitstats.org>",
            "author-time": "1664823233",
            "author-tz": "+0200",
            "committer": "Servio Tullio",
            "committer-mail": "<servio.tullio@gitstats.org>",
            "committer-time": "1692862967",
            "committer-tz": "+0300",
            "content": "        content 3",
            "filename": "blame_2",
            "hash": "ae69f55b7f137e8ff9056560841d558f93e018a3",
            "summary": "summary 3",
        },
        {
            "author": "Tarquinio Prisco",
            "author-mail": "<tarquinio.prisco@gitstats.org>",
            "author-time": "1664823234",
            "author-tz": "+0200",
            "committer": "Servio Tullio",
            "committer-mail": "<servio.tullio@gitstats.org>",
            "committer-time": "1692862967",
            "committer-tz": "+0300",
            "content": "        content 4",
            "filename": "blame_2",
            "hash": "ae69f55b7f138e8ff9056560841d558f93e018a3",
            "summary": "summary 4",
        },
    ]
