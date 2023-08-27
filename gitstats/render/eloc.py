from gitstats.data.model.file import File
from gitstats.render.model.table import Table
from gitstats.stats.commits_and_impact import count_commits_and_impact_by_author


async def get_edited_lines_of_code_and_stability_by_author() -> Table:
    table = Table("author", "edited line of code", "stability %")
    for author, cai in (await count_commits_and_impact_by_author(__only_interesting_source)).items():
        table.add_row(author.name, cai.eloc, __truncate(cai.stability))
    table.sort(column=1, reverse=True)
    table.add_total_row()
    table.update(-1, 0, "total")
    table.update(-1, -1, "")
    return table


async def get_edited_lines_of_code_by_author() -> Table:
    table = Table("author", "edited line of code")
    for author, commits_and_impact in (await count_commits_and_impact_by_author(__only_interesting_source)).items():
        table.add_row(author.name, commits_and_impact.eloc)
    table.sort(column=1, reverse=True)
    table.limit(7, others=True)
    table.update(-1, 0, "others")

    return table


def __only_interesting_source(file: File | None) -> bool:
    return (
        file is not None
        and file.is_src()
        and any(
            [
                file.is_groovy(),
                file.is_java(),
                file.is_javascript(),
                file.is_kotlin(),
                file.is_python(),
                file.is_rust(),
                file.is_typescript(),
                file.is_vue(),
            ]
        )
    )


def __truncate(f: float, n: int = 2) -> float:
    return float(format(f, f".{n}f"))
