from gitstats.data.authors import get_authors
from gitstats.render.model.table import Table


async def get_cemetery() -> list[Table]:
    dead = sorted(
        [author for author in await get_authors() if author.is_dead()],
        key=lambda author: author.end,
    )
    cemetery = []
    for d in dead:
        table = Table()
        table.add_row(d.name, d.username, d.start.strftime("%Y-%m-%d"), d.end.strftime("%Y-%m-%d"))
        cemetery.append(table)
    return cemetery
