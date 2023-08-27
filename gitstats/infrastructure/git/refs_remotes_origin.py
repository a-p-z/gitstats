from asyncio import get_event_loop
from typing import Any

from aiocache import cached
from git import Git

from gitstats.infrastructure.git import REF_FORMAT
from gitstats.infrastructure.git import REF_REMOTE_PATTERN
from gitstats.infrastructure.logging import logger
from gitstats.infrastructure.scope import application_scope


@cached()
async def refs_remotes_origin() -> list[dict[str, Any]]:
    git = application_scope.resolve(Git)
    event_loop = get_event_loop()
    for_each_ref = await event_loop.run_in_executor(
        None, lambda: git.for_each_ref("refs/remotes/origin", format=REF_FORMAT)
    )
    parsed = [__parse(line) for line in for_each_ref.split("\n")]
    return [remote for remote in parsed if remote]


def __parse(line: str) -> dict[str, str] | None:
    match = REF_REMOTE_PATTERN.search(line)
    if not match:
        logger.warning("unable to parse %s", line)
        return None

    name, author_name, author_email, date = match.groups()
    return {
        "name": name,
        "author-name": author_name,
        "author-email": author_email.strip("<>").lower(),
        "date": date,
    }
