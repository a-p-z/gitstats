from aiocache import cached

from gitstats.data.authors import get_authors_by_email
from gitstats.data.model.shortlog import ShortLog
from gitstats.infrastructure.git.shortlog import shortlog_merges
from gitstats.infrastructure.git.shortlog import shortlog_no_merges
from gitstats.infrastructure.logging import logger


@cached()
async def get_commits() -> list[ShortLog]:
    logger.info("getting commits")
    return [await __shortlog_decoder(shortlog) for shortlog in await shortlog_no_merges()]


@cached()
async def get_merges() -> list[ShortLog]:
    logger.info("getting merges")
    return [await __shortlog_decoder(shortlog) for shortlog in await shortlog_merges()]


async def __shortlog_decoder(obj: dict) -> ShortLog:
    author = (await get_authors_by_email())[obj["author-email"].strip("<>").lower()]
    return ShortLog(author, obj["commits"])
