from collections import defaultdict

from gitstats.data.logs import get_logs
from gitstats.data.model.author import Author
from gitstats.data.model.author import Reviewer
from gitstats.data.reviewers import get_reviewers
from gitstats.infrastructure.logging import logger


async def count_reviews_by_reviewer_and_author() -> dict[Reviewer, dict[Author, int]]:
    logger.info("count reviews by reviewer and author")
    reviewers_ = await get_reviewers()
    reviewer_author_reviews: dict[Reviewer, dict[Author, int]] = defaultdict(lambda: defaultdict(int))

    for log in await get_logs():
        for reviewer in __get_reviewers(log.subject, reviewers_):
            reviewer_author_reviews[reviewer][log.author] += 1
    return reviewer_author_reviews


def __get_reviewers(subject: str, reviewers: list[Reviewer]) -> list[Reviewer]:
    return [
        reviewer
        for reviewer in reviewers
        if any(
            [
                reviewer.name in subject,
                reviewer.email.split("@", 1)[0] in subject,
                reviewer.username is not None and reviewer.username in subject,
            ]
        )
    ]
