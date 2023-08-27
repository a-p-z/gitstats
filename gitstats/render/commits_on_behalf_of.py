from gitstats.render.model.table import Table
from gitstats.stats.commits_on_behalf_of import count_commits_on_behalf_of


async def get_commits_on_behalf_of() -> Table | None:
    commits_on_behalf_of = await count_commits_on_behalf_of()
    if not commits_on_behalf_of:
        return None
    authors = sorted(
        {
            author
            for commits_on_behalf_of in commits_on_behalf_of.values()
            for author in commits_on_behalf_of.keys()
            if not author.is_dead()
        }
    )
    table = Table("    ┌─> author\ncommitter", *[author.name for author in authors], "total")
    for committer in sorted(commits_on_behalf_of.keys()):
        if committer.is_dead():
            continue
        values = commits_on_behalf_of[committer]
        table.add_row(committer.name, *[values.get(author, 0) if author != committer else 0 for author in authors])
    table.add_total_row()
    table.add_total_column()
    table.update(-1, 0, "total")
    return table
