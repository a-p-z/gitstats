from collections import defaultdict
from collections.abc import Callable
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from gitstats.data.authors import get_authors
from gitstats.data.blames import get_blames
from gitstats.data.logs import get_logs
from gitstats.data.model.author import Author
from gitstats.data.model.file import File
from gitstats.data.model.log import Log
from gitstats.data.model.numstat import Numstat
from gitstats.data.model.shortlog import ShortLog
from gitstats.data.numstats import get_numstats
from gitstats.data.shortlog import get_commits
from gitstats.data.shortlog import get_merges
from gitstats.infrastructure.logging import logger
from gitstats.stats.model.commits_and_impact import CommitsAndImpact
from gitstats.stats.utils import group_by
from gitstats.stats.utils import group_by_by

STEP2STRF = {"1d": "%Y-%m-%d", "1m": "%Y-%m", "1y": "%Y"}


async def count_commits() -> dict[Author, int]:
    def fk(short_log: ShortLog) -> Author:
        return short_log.author

    def fv(short_logs: list[ShortLog]) -> int:
        return sum([short_log.commits for short_log in short_logs])

    return group_by(await get_commits(), fk, fv)


async def count_merges() -> dict[Author, int]:
    def fk(short_log: ShortLog) -> Author:
        return short_log.author

    def fv(short_logs: list[ShortLog]) -> int:
        return sum([short_log.commits for short_log in short_logs])

    return group_by(await get_merges(), fk, fv)


async def count_commits_and_impact_by_author(
    f: Callable[[File | None], bool] = lambda _file: True
) -> dict[Author, CommitsAndImpact]:
    logger.info("counting commits and impact by author")

    eloc_by_author = group_by(
        await get_blames(),
        lambda blame: blame.author,
        lambda blames: len([blame for blame in blames if f(blame.file)]),
    )
    total_impact = sum([numstat.impact for numstat in await get_numstats() if f(numstat.file)])

    def fk(numstat: Numstat) -> Author:
        return numstat.author

    def fv(numstats: list[Numstat]) -> CommitsAndImpact:
        merges = len({numstat.hash for numstat in numstats if numstat.is_merge() and f(numstat.file)})
        commits = len({numstat.hash for numstat in numstats if numstat.is_commit() and f(numstat.file)})
        insertions = sum([numstat.insertions for numstat in numstats if f(numstat.file)])
        deletions = sum([numstat.deletions for numstat in numstats if f(numstat.file)])
        eloc = eloc_by_author.get(numstats[0].author, 0) if numstats else 0
        return CommitsAndImpact(commits, insertions, deletions, merges, total_impact, eloc)

    return group_by(await get_numstats(), fk, fv)


async def cumulate_commits_and_impact_over_time_by_author(
    start: datetime, end: datetime, step: str, heritage: dict[Author, CommitsAndImpact]
) -> dict[str, dict[Author, CommitsAndImpact]]:
    if start >= end:
        return dict()
    logger.info("cumulating commits and impact over time by author")

    fmt = STEP2STRF.get(step, "1m")

    def fk1(log: Log) -> str:
        return log.date.astimezone(UTC).strftime(fmt)

    def fk2(log: Log) -> Author:
        return log.author

    def fv(logs_: list[Log]) -> CommitsAndImpact:
        merges = len([log for log in logs_ if log.is_merge()])
        commits = len([log for log in logs_ if log.is_commit()])
        insertions = sum([log.insertions for log in logs_])
        deletions = sum([log.deletions for log in logs_])
        return CommitsAndImpact(commits, insertions, deletions, merges)

    logs = [log for log in await get_logs() if start <= log.date <= end]
    commits_and_impact_by_period_and_author = group_by_by(logs, fk1, fk2, fv)

    cumulated: dict[str, dict[Author, CommitsAndImpact]] = defaultdict(dict)
    periods = __period_range(start, end, step)
    for i, period in enumerate(periods):
        for author in await get_authors():
            previous = cumulated[periods[i - 1]][author] if i > 0 else heritage.get(author, CommitsAndImpact(0, 0, 0))
            current = commits_and_impact_by_period_and_author.get(period, {}).get(author, CommitsAndImpact(0, 0, 0))
            cumulated[period][author] = previous + current

    return cumulated


async def count_commits_and_impact_over_time_by_author(
    start: datetime, end: datetime, step: str
) -> dict[str, dict[Author, CommitsAndImpact]]:
    if start >= end:
        return dict()

    logger.info("counting commits and impact over time by author with a step of %s", step)

    fmt = STEP2STRF.get(step, "1m")

    def fk1(log: Log) -> str:
        return log.date.astimezone(UTC).strftime(fmt)

    def fk2(log: Log) -> Author:
        return log.author

    def fv(logs_: list[Log]) -> CommitsAndImpact:
        merges = len([log for log in logs_ if log.is_merge()])
        commits = len([log for log in logs_ if log.is_commit()])
        insertions = sum([log.insertions for log in logs_])
        deletions = sum([log.deletions for log in logs_])
        return CommitsAndImpact(commits, insertions, deletions, merges)

    logs = [log for log in await get_logs() if start <= log.date <= end]
    grouped = group_by_by(logs, fk1, fk2, fv)
    period_range = __period_range(start, end, step)
    return {period: grouped.get(period, dict()) for period in period_range}


async def count_commits_and_impact_over_time(start: datetime, end: datetime, step: str) -> dict[str, CommitsAndImpact]:
    if start >= end:
        return dict()
    logger.info("counting commits and impact over time with a step of %s", step)

    fmt = STEP2STRF.get(step, "1m")

    def fk(log: Log) -> str:
        return log.date.astimezone(UTC).strftime(fmt)

    def fv(logs: list[Log]) -> CommitsAndImpact:
        merges = len([log for log in logs if log.is_merge()])
        commits = len([log for log in logs if log.is_commit()])
        insertions = sum([log.insertions for log in logs])
        deletions = sum([log.deletions for log in logs])
        return CommitsAndImpact(commits, insertions, deletions, merges)

    grouped = group_by([log for log in await get_logs() if start <= log.date <= end], fk, fv)
    period_range = __period_range(start, end, step)
    return {period: grouped.get(period, CommitsAndImpact(0, 0, 0)) for period in period_range}


async def count_commits_and_impact_by_file() -> dict[File, CommitsAndImpact]:
    logger.info("counting commits and impact by filename")

    def fk(numstat: Numstat) -> File:
        return numstat.file if numstat.is_commit() and numstat.file else File("merge")

    def fv(numstats: list[Numstat]) -> CommitsAndImpact:
        commits = len([numstat.insertions for numstat in numstats if numstat.is_commit()])
        insertions = sum([numstat.insertions for numstat in numstats if numstat.is_commit()])
        deletions = sum([numstat.deletions for numstat in numstats if numstat.is_commit()])
        return CommitsAndImpact(commits, insertions, deletions)

    return group_by(await get_numstats(), fk, fv)


async def count_commits_and_impact_by_extension() -> dict[str, CommitsAndImpact]:
    logger.info("counting commits and impact by extension")

    def fk(numstat: Numstat) -> str:
        return numstat.file.suffix if numstat.is_commit() and numstat.file and numstat.file.suffix else "NO EXT"

    def fv(numstats: list[Numstat]) -> CommitsAndImpact:
        commits = len([numstat for numstat in numstats if numstat.is_commit()])
        insertions = sum([numstat.insertions for numstat in numstats if numstat.is_commit()])
        deletions = sum([numstat.deletions for numstat in numstats if numstat.is_commit()])
        return CommitsAndImpact(commits, insertions, deletions)

    return group_by(await get_numstats(), fk, fv)


def __period_range(start: datetime, end: datetime, step: str = "1m") -> list[str]:
    if step == "1d":
        return __days_range(start, end)

    if step == "1y":
        return __years_range(start, end)

    return __months_range(start, end)


def __days_range(start: datetime, end: datetime) -> list[str]:
    delta: timedelta = end - start
    range_ = range(delta.days + 1)
    fmt = "%Y-%m-%d"
    return [(start + timedelta(days=days)).strftime(fmt) for days in range_]


def __years_range(start: datetime, end: datetime) -> list[str]:
    delta: int = end.year - start.year
    range_ = range(delta + 1)
    return [str(start.year + years) for years in range_]


def __months_range(start: datetime, end: datetime) -> list[str]:
    delta: relativedelta = relativedelta(end, start)
    range_ = range(delta.years * 12 + delta.months + 1)
    fmt = "%Y-%m"
    return [(start + relativedelta(months=months)).strftime(fmt) for months in range_]
