from collections.abc import Callable

from gitstats.data.authors import Author
from gitstats.data.blames import get_blames
from gitstats.data.model.blame import Blame
from gitstats.infrastructure.logging import logger
from gitstats.stats.utils import group_by


async def count_empty_lines_of_code_by_author(f: Callable[[Blame], bool] = lambda _blame: True) -> dict[Author, int]:
    def fv(blames: list[Blame]) -> int:
        return len([blame for blame in blames if blame.content_is_empty() and f(blame)])

    return group_by(await get_blames(), lambda blame: blame.author, fv)


async def count_edited_lines_of_code_by_author(f: Callable[[Blame], bool]) -> dict[Author, int]:
    logger.info("count edited lines of code by author")

    def fv(blames: list[Blame]) -> int:
        return len([blame for blame in blames if f(blame)])

    return group_by(await get_blames(), lambda blame: blame.author, fv)
