from asyncio import get_event_loop

from aiocache import cached
from git import Git

from gitstats.infrastructure.scope import application_scope


@cached()
async def files() -> list[str]:
    git = application_scope.resolve(Git)
    event_loop = get_event_loop()
    output = await event_loop.run_in_executor(None, git.ls_files)
    return output.split("\n")
