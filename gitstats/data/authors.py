from collections.abc import Iterable
from datetime import datetime

from aiocache import cached

from gitstats.data.model.author import Author
from gitstats.infrastructure.git.log import log
from gitstats.infrastructure.git.usernames import get_usernames_by_email
from gitstats.infrastructure.logging import logger


@cached()
async def get_authors() -> list[Author]:
    logger.info("getting authors")
    usernames_by_email = await get_usernames_by_email()
    return [
        Author(a.name, a.email, a.start, a.end, usernames_by_email.get(a.email)) for a in await __get_authors_from_log()
    ]


@cached()
async def get_authors_by_email() -> dict[str, Author]:
    logger.info("grouping authors by email")
    return {author.email: author for author in await get_authors()}


async def __get_authors_from_log() -> Iterable[Author]:
    logger.info("getting authors from logs")

    authors: dict[str, Author] = {}
    for log_ in await log():
        name = log_["author-name"]
        email = log_["author-email"].strip("<>").lower()
        date = datetime.fromisoformat(log_["author-date"])
        if email not in authors.keys():
            authors[email] = Author(name, email, date, date, None)
        else:
            start = min(authors[email].start, date)
            end = max(authors[email].end, date)
            authors[email] = Author(name, email, start, end, None)

    return authors.values()
