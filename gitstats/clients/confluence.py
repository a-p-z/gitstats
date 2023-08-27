from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from gitstats.infrastructure.logging import logger


@dataclass(frozen=True)
class ConfluenceClient:
    base_uri: str
    username: str
    password: str

    @property
    def __auth(self) -> tuple[str, str]:
        return self.username, self.password

    async def update(self, id_: int, title: str, value: str, version: int):
        logger.info("updating page %s", id_)
        url = f"{self.base_uri}/rest/api/content/{id_}"
        headers = {"Content-type": "application/json"}
        json_ = {
            "id": str(id_),
            "type": "page",
            "title": title,
            "body": {"storage": {"value": value, "representation": "storage"}},
            "version": {"number": version},
        }
        async with ClientSession() as session:
            async with session.put(url, headers=headers, auth=self.__auth, json=json_) as response:
                response.raise_for_status()

    async def wiki2storage(self, value: str) -> str:
        logger.info("converting wiki to storage")
        url = f"{self.base_uri}/rest/api/contentbody/convert/storage"
        headers = {"Content-type": "application/json"}
        json_ = {"value": value, "representation": "wiki"}
        async with ClientSession() as session:
            async with session.post(url, headers=headers, auth=self.__auth, json=json_) as response:
                response.raise_for_status()
                body = await response.json()
                return body["value"]

    async def get_content_by_id(self, id_: int) -> Any:
        logger.info("getting page %s", id_)
        url = f"{self.base_uri}/rest/api/content/{id_}"
        async with ClientSession() as session:
            async with session.get(url, auth=self.__auth) as response:
                response.raise_for_status()
                return await response.json()
