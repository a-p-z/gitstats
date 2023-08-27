from aiocache import cached

from gitstats.data.model.file import File
from gitstats.infrastructure.git.files import files
from gitstats.infrastructure.logging import logger


@cached()
async def get_files() -> list[File]:
    logger.info("getting files")
    return [File(filename) for filename in await files()]
