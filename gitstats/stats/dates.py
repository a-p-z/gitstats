from datetime import UTC
from datetime import datetime

from aiocache import cached

from gitstats.data.logs import get_logs


@cached()
async def get_start_date() -> datetime:
    return min([log.date for log in await get_logs()]).astimezone(UTC)


@cached()
async def get_last_update() -> datetime:
    return max([log.date for log in await get_logs()]).astimezone(UTC)
