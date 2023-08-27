from asyncio import get_event_loop
from re import Match
from typing import Any

from aiocache import cached
from git import Git

from gitstats.infrastructure.git import SHORT_LOGS_PATTERN
from gitstats.infrastructure.scope import application_scope


@cached()
async def shortlog_no_merges() -> list[dict[str, Any]]:
    git = application_scope.resolve(Git)
    event_loop = get_event_loop()
    raw_short_logs = await event_loop.run_in_executor(
        None, lambda: git.shortlog("HEAD", summary=True, email=True, numbered=True, no_merges=True)
    )
    return __parse(raw_short_logs.split("\n"))


@cached()
async def shortlog_merges() -> list[dict[str, Any]]:
    git = application_scope.resolve(Git)
    event_loop = get_event_loop()
    raw_short_logs = await event_loop.run_in_executor(
        None, lambda: git.shortlog("HEAD", summary=True, email=True, numbered=True, merges=True)
    )
    return __parse(raw_short_logs.split("\n"))


def __parse(raw_short_logs: list[str]) -> list[dict[str, Any]]:
    short_log_matches = map(lambda line: SHORT_LOGS_PATTERN.match(line.rstrip()), raw_short_logs)
    filtered_short_log_matches = [
        short_log_match for short_log_match in short_log_matches if short_log_match is not None
    ]
    return [__raw_short_log_to_short_log(m) for m in filtered_short_log_matches]


def __raw_short_log_to_short_log(short_log_match: Match[str]) -> dict[str, Any]:
    commits = int(short_log_match.group(1))
    name = short_log_match.group(2)
    email = short_log_match.group(3).lower()
    return {"author-name": name, "author-email": email.lower(), "commits": commits}
