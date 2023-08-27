from collections.abc import Iterable
from datetime import datetime

from aiocache import cached

from gitstats.data.model.author import Committer
from gitstats.infrastructure.git.log import log
from gitstats.infrastructure.git.usernames import get_usernames_by_email
from gitstats.infrastructure.logging import logger


@cached()
async def get_committers() -> list[Committer]:
    logger.info("getting committers")
    usernames_by_email = await get_usernames_by_email()
    return [
        Committer(c.name, c.email, c.start, c.end, usernames_by_email.get(c.email))
        for c in await __get_committers_from_log()
    ]


@cached()
async def get_committers_by_email() -> dict[str, Committer]:
    logger.info("grouping committers by email")
    return {committer.email: committer for committer in await get_committers()}


async def __get_committers_from_log() -> Iterable[Committer]:
    logger.info("getting committers from logs")

    committers: dict[str, Committer] = {}
    for log_ in await log():
        name = log_["committer-name"]
        email = log_["committer-email"].strip("<>").lower()
        date = datetime.fromisoformat(log_["committer-date"])
        if email not in committers.keys():
            committers[email] = Committer(name, email, date, date, None)
        else:
            start = min(committers[email].start, date)
            end = max(committers[email].end, date)
            committers[email] = Committer(name, email, start, end, None)

    return committers.values()
