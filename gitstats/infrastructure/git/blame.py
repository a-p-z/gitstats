from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path

from aiocache import cached
from git import Git

from gitstats.infrastructure.git import HASH_PATTERN
from gitstats.infrastructure.git.files import files
from gitstats.infrastructure.logging import logger
from gitstats.infrastructure.scope import application_scope


@cached()
async def blame() -> list[dict[str, str]]:
    files_ = await files()
    git = application_scope.resolve(Git)

    with ThreadPoolExecutor(thread_name_prefix="Blamer") as thread_pool_executor:
        futures = [thread_pool_executor.submit(__blame, file, git) for file in files_]

    results = [future.result() for future in as_completed(futures)]

    blames = [item for result in results for item in result]
    return blames


def __blame(file: str, git: Git) -> list[dict[str, str]]:
    path = Path(str(git.working_dir)) / file
    if not path.exists():
        logger.warning("skipping blame on not existing file %s", file)
        return list()

    if __is_empty(path):
        logger.warning("skipping blame on empty file %s", file)
        return list()

    if __is_binary(path):
        logger.warning("skipping blame on binary file %s", file)
        return list()

    i = -1
    result: list[dict[str, str]] = []
    for line in git.blame(file, line_porcelain=True).split("\n"):
        if not line or line == "boundary":
            continue
        if HASH_PATTERN.match(line):
            i += 1
            result.append({"hash": line[:40]})
            continue
        if line.startswith("\t"):
            result[i]["content"] = line[1:]
            continue

        key, value = line.split(" ", 1)
        result[i][key] = value

    return result


def __is_empty(path: Path) -> bool:
    with path.open("rb") as file:
        return file.read(1) == b""


def __is_binary(path: Path) -> bool:
    try:
        with path.open("tr") as file:
            file.read(1)
    except UnicodeDecodeError:
        return True
    return False
