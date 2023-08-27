from datetime import UTC
from datetime import datetime
from datetime import timedelta

from gitstats.data.references import get_origin_remote_references
from gitstats.render.model.table import Table
from gitstats.stats.references import count_references_by_author


async def get_forgotten_refs() -> Table | None:
    refs = [ref for ref in await get_origin_remote_references() if ref.date < datetime.now(tz=UTC) - timedelta(30)]
    if not refs:
        return None
    table = Table("ref", "last commit date", "author")
    for ref in refs:
        table.add_row(
            ref.name.replace("refs/remotes/origin/", ""),
            ref.date.astimezone(UTC).strftime("%Y-%m-%d"),
            ref.author.name,
        )
    table.sort(column=1)
    table.limit(10)
    return table


async def get_total_refs_over_author() -> Table:
    table = Table("author", "total")
    for author, refs in (await count_references_by_author()).items():
        table.add_row(author.name, refs)
    table.sort(column=1, reverse=True)
    table.limit(7, others=True)
    table.update(-1, 0, "others")
    return table
