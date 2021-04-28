import logging

from core import process

GIT_REV_LIST_NO_MERGES_COUNT_HEAD = "git rev-list --no-merges --count HEAD"


def count_commits() -> int:
    logging.info("counting commits")
    logging.info("executing %s", GIT_REV_LIST_NO_MERGES_COUNT_HEAD)
    return int(process.execute(GIT_REV_LIST_NO_MERGES_COUNT_HEAD))
