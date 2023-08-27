from datetime import datetime

from aiocache import cached

from gitstats.data.authors import get_authors_by_email
from gitstats.data.model.author import Author
from gitstats.data.model.ref import Ref
from gitstats.infrastructure.git.refs_remotes_origin import refs_remotes_origin
from gitstats.infrastructure.logging import logger


@cached()
async def get_origin_remote_references() -> list[Ref]:
    logger.info("getting references")
    return [await __ref_decoder(ref) for ref in await refs_remotes_origin() if ref]


async def __ref_decoder(obj: dict) -> Ref:
    authors_by_email = await get_authors_by_email()
    email = obj["author-email"].strip("<>").lower()
    unknown_author = Author("unknown", obj["author-email"])
    author = authors_by_email.get(email, unknown_author)
    return Ref(obj["name"], author, datetime.strptime(obj["date"], "%Y-%m-%d %H:%M:%S %z"))
