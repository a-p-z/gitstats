from gitstats.render.model.table import Table
from gitstats.stats.extensions import count_files_by_extension


async def get_files_by_extension() -> Table:
    table = Table("extension", "total")
    for extension, value in (await count_files_by_extension()).items():
        table.add_row(extension, value)
    table.sort(column=1, reverse=True)
    table.limit(7, others=True)
    table.update(-1, 0, "others")
    return table
