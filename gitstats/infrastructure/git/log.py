from asyncio import get_event_loop

from aiocache import cached
from git import Git

from gitstats.infrastructure.git import LOG_NUMSTAT_PRETTY
from gitstats.infrastructure.git import LOG_PRETTY
from gitstats.infrastructure.scope import application_scope


@cached()
async def log() -> list[dict[str, str]]:
    git = application_scope.resolve(Git)

    event_loop = get_event_loop()
    output = await event_loop.run_in_executor(None, lambda: git.log(date="iso8601", pretty=LOG_PRETTY))

    i = -1
    result: list[dict[str, str]] = []
    for line in output.split("\n"):
        if not line:
            continue
        key, value = line.split(" ", 1)
        if key == "hash":
            i += 1
            result.append({})
        result[i][key] = value

    return result


@cached()
async def log_numstat() -> list[dict[str, str | int]]:
    git = application_scope.resolve(Git)

    event_loop = get_event_loop()
    output = await event_loop.run_in_executor(
        None, lambda: git.log(date="iso8601", numstat=True, pretty=LOG_NUMSTAT_PRETTY)
    )
    result = []
    hash_ = None
    for line in output.split("\n"):
        if not line:
            continue
        if line.startswith("hash"):
            _, hash_ = line.split(" ", 1)
            continue
        insertions, deletions, filename = line.replace("-", "0").split("\t", 2)
        result.append({"hash": hash_, "insertions": int(insertions), "deletions": int(deletions), "filename": filename})

    return result
