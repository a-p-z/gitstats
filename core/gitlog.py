import logging
from typing import List

from core import process, persistence
from core.model.commit import Commit
from core.model.diffstat import Diffstat
from core.model.numstat import Numstat

GIT_LOG_NUMSTAT_NO_MERGES = "git log" \
                            " --pretty=tformat:'.:*-*:.%n%h%n%aI%n%s%n%aN%n%aE%n%cN%n%cE'" \
                            " --numstat" \
                            " --no-merges" \
                            " --date=iso8601"


def git_log_numstat_no_merges(load=False) -> List[Numstat]:
    if not load:
        logging.info("git log numstat no-merges")
        raw_logs = __git_log_numstat_no_merge()
        numstat = __raw_logs_to_numstat(raw_logs)
        persistence.dump_numstat(numstat)
        return numstat

    try:
        return persistence.load_numstat()
    except (FileNotFoundError, EOFError):
        return git_log_numstat_no_merges(False)


def __raw_logs_to_numstat(raw_logs) -> List[Numstat]:
    commits = __raw_logs_to_commits(raw_logs)
    numstat = list()
    for commit in commits:
        numstat_list = __commit_to_numstat_list(commit)
        numstat.extend(numstat_list)
    return numstat


def __git_log_numstat_no_merge() -> List[str]:
    logging.info("executing %s", GIT_LOG_NUMSTAT_NO_MERGES)
    return process.execute(GIT_LOG_NUMSTAT_NO_MERGES).split(".:*-*:.\n")[1:]


def __raw_logs_to_commits(logs: List[str]) -> List[Commit]:
    return list(map(lambda log: Commit.of(log), logs))


def __commit_to_numstat_list(commit: Commit) -> List[Numstat]:
    if len(commit.diffstats) == 0:
        return [Numstat.of(commit, Diffstat("", 0, 0))]
    return list(map(lambda diffstat: Numstat.of(commit, diffstat), commit.diffstats))
