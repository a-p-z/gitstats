from asyncio import get_event_loop

from aiocache import cached
from git import Git

from gitstats.infrastructure.scope import application_scope


@cached()
async def rev_list_no_merges_count_head() -> int:
    git = application_scope.resolve(Git)
    event_loop = get_event_loop()
    rev_list = await event_loop.run_in_executor(None, lambda: git.rev_list("HEAD", no_merges=True, count=True))
    return int(rev_list)
