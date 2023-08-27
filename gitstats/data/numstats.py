from aiocache import cached

from gitstats.data.logs import get_logs
from gitstats.data.model.numstat import Numstat
from gitstats.infrastructure.logging import logger


@cached()
async def get_numstats() -> list[Numstat]:
    logger.info("getting numstats")
    return [
        Numstat(log.hash, log.parent, log.date, log.subject, log.author, log.committer)
        for log in await get_logs()
        if not log.diffstats
    ] + [
        Numstat(
            log.hash,
            log.parent,
            log.date,
            log.subject,
            log.author,
            log.committer,
            diffstat.file,
            diffstat.insertions,
            diffstat.deletions,
        )
        for log in await get_logs()
        for diffstat in log.diffstats
    ]
