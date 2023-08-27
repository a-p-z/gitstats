from unittest.mock import MagicMock
from unittest.mock import patch

from aiohttp import ClientSession
from pytest import mark

from gitstats.clients.confluence import ConfluenceClient
from tests import a_base_uri
from tests import a_content_id
from tests import a_password
from tests import a_title
from tests import a_username
from tests import a_value
from tests import a_version


@mark.asyncio
@patch.object(ClientSession, "put")
async def test_update(mock_put: MagicMock):
    base_uri = a_base_uri()
    content_id = a_content_id()
    username = a_username()
    password = a_password()
    title = a_title()
    value = a_value()
    version = a_version()

    url = f"{base_uri}/rest/api/content/{content_id}"
    headers = {"Content-type": "application/json"}
    auth = (username, password)
    body = {
        "id": str(content_id),
        "type": "page",
        "title": title,
        "body": {"storage": {"value": value, "representation": "storage"}},
        "version": {"number": version},
    }

    client = ConfluenceClient(base_uri, username, password)
    await client.update(content_id, title, value, version)

    mock_put.assert_called_once_with(url, headers=headers, auth=auth, json=body)


@mark.asyncio
@patch.object(ClientSession, "post")
async def test_wiki2storage(mock_post: MagicMock):
    base_uri = a_base_uri()
    username = a_username()
    password = a_password()
    value = a_value()

    url = f"{base_uri}/rest/api/contentbody/convert/storage"
    headers = {"Content-type": "application/json"}
    auth = (username, password)
    json_ = {"value": value, "representation": "wiki"}

    mock_post.return_value.__aenter__.return_value.json.return_value = {"value": "storage"}

    client = ConfluenceClient(base_uri, username, password)
    response = await client.wiki2storage(value)

    assert response == "storage"
    mock_post.assert_called_once_with(url, headers=headers, auth=auth, json=json_)


@mark.asyncio
@patch.object(ClientSession, "get")
async def test_get_content_by_id(mock_get: MagicMock):
    base_uri = a_base_uri()
    username = a_username()
    password = a_password()
    content_id = a_content_id()

    url = f"{base_uri}/rest/api/content/{content_id}"
    auth = (username, password)

    mock_get.return_value.__aenter__.return_value.json.return_value = {"any": "any"}

    client = ConfluenceClient(base_uri, username, password)
    response = await client.get_content_by_id(content_id)

    assert response == {"any": "any"}
    mock_get.assert_called_once_with(url, auth=auth)
