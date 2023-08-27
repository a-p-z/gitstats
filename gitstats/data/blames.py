from aiocache import cached

from gitstats.data.authors import get_authors_by_email
from gitstats.data.committers import get_committers_by_email
from gitstats.data.model.blame import Blame
from gitstats.data.model.file import File
from gitstats.infrastructure.git.blame import blame
from gitstats.infrastructure.logging import logger


@cached()
async def get_blames() -> list[Blame]:
    logger.info("getting blames")
    return [await __blame_decoder(b) for b in await blame()]


async def __blame_decoder(obj: dict) -> Blame:
    authors_by_email = await get_authors_by_email()
    author = authors_by_email.get(obj["author-mail"].strip("<>").lower())
    committers_by_email = await get_committers_by_email()
    committer = committers_by_email.get(obj["committer-mail"].strip("<>").lower())
    file = File(obj["filename"])
    return Blame(obj["hash"], author, committer, obj["summary"], file, obj["content"])
