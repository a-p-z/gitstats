from gitstats.data.authors import get_authors
from gitstats.render.model.table import Table
from gitstats.stats.reviews import count_reviews_by_reviewer_and_author


def get_reviews() -> Table | None:
    reviews_by_reviewer_and_author = count_reviews_by_reviewer_and_author()
    if not reviews_by_reviewer_and_author:
        return None
    authors = sorted([author for author in get_authors() if not author.is_dead()])
    table = Table("    ┌─> author\nreviewer", *[author.name for author in authors])
    for reviewer, author_reviews in reviews_by_reviewer_and_author.items():
        if reviewer.is_dead():
            continue
        table.add_row(reviewer.name, *[author_reviews[author] for author in authors])
    table.add_total_row()
    table.update(-1, 0, "total")
    table.add_total_column()
    return table
