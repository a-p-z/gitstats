from gitstats.data.files import get_files
from gitstats.infrastructure.logging import logger
from gitstats.stats.utils import group_by


async def count_files_by_extension() -> dict[str, int]:
    logger.info("count files by extension")
    return group_by(await get_files(), lambda file: file.suffix if file.suffix else "NO EXT", len)
