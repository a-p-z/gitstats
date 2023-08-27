from datetime import UTC
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from gitstats.data.authors import get_authors
from gitstats.data.logs import get_logs
from gitstats.render.model.table import Table
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_author
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_extension
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_file
from gitstats.stats.commits_and_impact import count_commits_and_impact_over_time
from gitstats.stats.commits_and_impact import count_commits_and_impact_over_time_by_author
from gitstats.stats.commits_and_impact import cumulate_commits_and_impact_over_time_by_author
from gitstats.stats.dates import get_last_update
from gitstats.stats.dates import get_start_date
from gitstats.stats.model.commits_and_impact import CommitsAndImpact


async def get_commits_and_impacts_by_author() -> Table:
    table = Table("author", "commits", "insertions", "deletions", "% of changes", "impact/commit")
    for author, commits_and_impact in (await count_commits_and_impact_by_author()).items():
        table.add_row(
            author.name,
            commits_and_impact.commits,
            commits_and_impact.insertions,
            commits_and_impact.deletions,
            __truncate(commits_and_impact.percentage_of_changes),
            int(commits_and_impact.impact_over_commit),
        )

    table.sort(column=1, reverse=True)
    table.add_total_row()
    table.update(-1, 0, "total")
    table.update(-1, -1, "")
    table.update(-1, -2, "")
    return table


async def get_commits_by_author() -> Table:
    table = Table("author", "commits")
    for author, commits_and_impact_ in (await count_commits_and_impact_by_author()).items():
        table.add_row(author.name, commits_and_impact_.commits)
    table.sort(column=1, reverse=True)
    table.limit(7, others=True)
    table.update(-1, 0, "others")
    return table


async def get_most_impactful_commits() -> Table:
    table = Table("date", "subject", "author", "number of file", "insertions", "deletions")

    def impact(row: tuple[str | int | float, ...]) -> int:
        insertions: int = row[4] if isinstance(row[4], int) else 0
        deletions: int = row[5] if isinstance(row[5], int) else 0
        return insertions + deletions

    for log in await get_logs():
        table.add_row(
            log.date.astimezone(UTC).strftime("%Y-%m-%d"),
            log.subject,
            log.author.name,
            len(log.diffstats),
            log.insertions,
            log.deletions,
        )
    table.sort(key=impact, reverse=True)
    table.limit(5)
    return table


async def get_cumulated_commits_over_time_by_author() -> Table:
    start_date_1 = await get_start_date()
    end_date_2 = await get_last_update()
    end_date_1 = max(
        end_date_2 - relativedelta(months=12, day=31, hour=23, minute=59, second=59),
        start_date_1,
    )
    start_date_2 = end_date_1 + timedelta(seconds=1)
    over_years = await cumulate_commits_and_impact_over_time_by_author(start_date_1, end_date_1, "1y", {})
    heritage = over_years.get(end_date_1.strftime("%Y"), {})
    over_months = await cumulate_commits_and_impact_over_time_by_author(start_date_2, end_date_2, "1m", heritage)

    cumulated = {**over_years, **over_months}
    authors = sorted(await get_authors(), key=lambda author: author.start)

    table = Table("period", *[author.name for author in authors])
    for period, commits_and_impact in cumulated.items():
        table.add_row(period, *[commits_and_impact[author].commits for author in authors])
    table.sort(column=0)
    return table


async def get_impact_over_time() -> Table:
    start_date_1 = await get_start_date()
    end_date_2 = await get_last_update()
    end_date_1 = max(
        end_date_2 - relativedelta(months=12, day=31, hour=23, minute=59, second=59),
        start_date_1,
    )
    start_date_2 = end_date_1 + timedelta(seconds=1)

    over_years = await count_commits_and_impact_over_time(start_date_1, end_date_1, "1y")
    over_months = await count_commits_and_impact_over_time(start_date_2, end_date_2, "1m")
    over_time = {**over_years, **over_months}

    table = Table("period", "insertions", "deletions")
    for period, commits_and_impact in over_time.items():
        table.add_row(period, commits_and_impact.insertions, commits_and_impact.deletions)
    table.sort(column=0)
    return table


async def get_commits_over_time_by_author() -> Table:
    start_date_1 = await get_start_date()
    end_date_2 = await get_last_update()
    end_date_1 = max(
        end_date_2 - relativedelta(months=12, day=31, hour=23, minute=59, second=59),
        start_date_1,
    )
    start_date_2 = end_date_1 + timedelta(seconds=1)

    over_years = await count_commits_and_impact_over_time_by_author(start_date_1, end_date_1, "1y")
    over_months = await count_commits_and_impact_over_time_by_author(start_date_2, end_date_2, "1m")
    over_time = {**over_years, **over_months}

    authors = sorted(await get_authors(), key=lambda author: author.start)
    table = Table("period", *[author.name for author in authors])

    for period, commits_and_impact in over_time.items():
        table.add_row(
            period,
            *[commits_and_impact.get(author, CommitsAndImpact(0, 0, 0)).commits for author in authors],
        )
    table.sort(column=0)
    return table


def get_most_frequently_committed_extensions() -> Table:
    table = Table("extension", "total")
    for (
        extension,
        commits_and_impact,
    ) in count_commits_and_impact_by_extension().items():
        table.add_row(extension, commits_and_impact.commits)
    table.sort(column=1, reverse=True)
    table.limit(10)
    return table


async def get_most_frequently_committed_filenames() -> Table:
    table = Table("file", "commits")
    for file, commits_and_impact in (await count_commits_and_impact_by_file()).items():
        table.add_row(str(file), commits_and_impact.commits)
    table.sort(column=1, reverse=True)
    table.limit(10)
    return table


def __truncate(f: float, n: int = 2) -> float:
    return float(format(f, f".{n}f"))
