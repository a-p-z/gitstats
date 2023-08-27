from datetime import datetime

from aiocache import cached

from gitstats.data.authors import get_authors_by_email
from gitstats.data.committers import get_committers_by_email
from gitstats.data.model.diffstat import Diffstat
from gitstats.data.model.file import File
from gitstats.data.model.log import Log
from gitstats.infrastructure.git.log import log
from gitstats.infrastructure.git.log import log_numstat
from gitstats.infrastructure.logging import logger
from gitstats.stats.utils import group_by


@cached()
async def get_logs() -> list[Log]:
    logger.info("getting logs")
    return [await __log_decoder(log_) for log_ in await log()]


@cached()
async def get_diffstats() -> list[Diffstat]:
    logger.info("getting diffstats")
    return [__diffstat_decoder(numstat) for numstat in await log_numstat()]


@cached()
async def get_diffstats_by_hash() -> dict[str, list[Diffstat]]:
    logger.info("getting diffstats by hash")
    diffstats = await get_diffstats()
    return group_by(diffstats, lambda diffstat: diffstat.hash, lambda x: x)


async def __log_decoder(obj: dict) -> Log:
    author = (await get_authors_by_email())[obj["author-email"].strip("<>").lower()]
    committer = (await get_committers_by_email())[obj["committer-email"].strip("<>").lower()]
    diffstats_by_hash = await get_diffstats_by_hash()
    date = datetime.fromisoformat(obj["author-date"])
    diffstats = diffstats_by_hash.get(obj["hash"], [])
    return Log(obj["hash"], obj["parent"], date, obj["subject"], author, committer, diffstats)


def __diffstat_decoder(obj: dict) -> Diffstat:
    file = File(obj["filename"])
    return Diffstat(obj["hash"], file, obj["insertions"], obj["deletions"])
