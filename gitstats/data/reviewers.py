from aiocache import cached

from gitstats.data.authors import get_authors
from gitstats.data.model.author import Reviewer
from gitstats.infrastructure.logging import logger


@cached()
async def get_reviewers() -> list[Reviewer]:
    logger.info("getting reviewers")
    return await get_authors()
