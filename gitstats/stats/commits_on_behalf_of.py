from aiocache import cached

from gitstats.data.logs import get_logs
from gitstats.data.model.author import Author
from gitstats.data.model.author import Committer
from gitstats.infrastructure.logging import logger
from gitstats.stats.utils import group_by_by


@cached()
async def count_commits_on_behalf_of() -> dict[Committer, dict[Author, int]]:
    logger.info("count commits on behalf of")
    return group_by_by(await get_logs(), lambda log: log.committer, lambda log: log.author, len)
