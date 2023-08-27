from gitstats.data.model.author import Author
from gitstats.data.references import get_origin_remote_references
from gitstats.infrastructure.logging import logger
from gitstats.stats.utils import group_by


async def count_references_by_author() -> dict[Author, int]:
    logger.info("counting references by author")
    return group_by(await get_origin_remote_references(), lambda ref: ref.author, len)
