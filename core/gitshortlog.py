import logging
import re
from typing import List, Dict

from core import process
from core.mailmap import Mailmap
from core.utilities import second_column, aggregate_and_sum

GIT_SHORTLOG_NO_MERGES = "git shortlog HEAD -s -e -n --no-merges"
GIT_SHORTLOG_MERGES = "git shortlog HEAD -s -e -n --merges"


def count_commits_by_author() -> List[List]:
    """
    :return: list of [author, commits]
    """
    logging.info("executing %s", GIT_SHORTLOG_NO_MERGES)
    raw_short_logs = process.execute(GIT_SHORTLOG_NO_MERGES).split("\n")
    logging.info("counting commits by author")
    short_logs = __raw_short_logs_to_short_logs(raw_short_logs)
    commits_by_author = aggregate_and_sum(short_logs, "author", "commits")
    author_commits = map(list, commits_by_author.items())
    return sorted(author_commits, key=second_column, reverse=True)


def count_merges_by_author() -> List[List]:
    """
    :return: list of [author, merges]
    """
    logging.info("executing %s", GIT_SHORTLOG_MERGES)
    raw_short_logs = process.execute(GIT_SHORTLOG_MERGES).split("\n")
    logging.info("counting merges by author")
    short_logs = __raw_short_logs_to_short_logs(raw_short_logs)
    merges_by_author = aggregate_and_sum(short_logs, "author", "commits")
    author_merges = map(list, merges_by_author.items())
    return sorted(author_merges, key=second_column, reverse=True)


def __raw_short_logs_to_short_logs(raw_short_logs: List[str]) -> List[Dict]:
    short_log_matches = map(lambda line: re.match(r"\s*(\d+)\t(.+) <(.+)>", line), raw_short_logs)
    short_log_matches = filter(lambda short_log_match: short_log_match, short_log_matches)
    return list(map(__raw_short_log_to_short_log, short_log_matches))


def __raw_short_log_to_short_log(short_log_match) -> Dict:
    name = short_log_match.group(2)
    email = short_log_match.group(3).lower()
    commits = int(short_log_match.group(1))
    author = Mailmap.get_or_default(name, email)
    return {"author": author, "commits": commits}

