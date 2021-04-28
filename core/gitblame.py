import logging
from typing import List

from core import process, persistence
from core.model.blame import Blame
from core.model.fileType import FileType
from core.percentageLogging import PercentageLogging

GIT_BLAME_LINE_PORCELAIN = "git blame --line-porcelain %s"


def git_blame(files, load=False) -> List[Blame]:
    if not load:
        logging.info("git blame")
        files = filter(lambda _file: FileType.any_match(FileType.all(), _file), files)
        files = list(files)
        blame = __git_blame_on_files(files)
        persistence.dump_blame(blame)
        return blame

    try:
        return persistence.load_blame()
    except (FileNotFoundError, EOFError):
        return git_blame(files, False)


def __git_blame_on_files(files: List[str]) -> List[Blame]:
    total = len(files)
    percentage_logging = PercentageLogging(10, total)
    blame = list()
    for i in range(total):
        percentage_logging.info(i, "blaming %3d%%")
        b = __git_blame_on_file(files[i])
        blame.extend(b)
    return blame


def __git_blame_on_file(file: str) -> List[Blame]:
    logging.debug("executing %s %s", GIT_BLAME_LINE_PORCELAIN, file)
    try:
        raw_blame = process.execute(GIT_BLAME_LINE_PORCELAIN % file).split("\n")
        raw_blame = __join_raw_blame(raw_blame)
        return __raw_blame_to_blame(raw_blame)
    except process.ProcessException as e:
        logging.warning("Error blaming %s: %s", file, e)
        return []


def __join_raw_blame(raw_blame: List[str]) -> List[str]:
    blame = list()
    tmp = list()

    for line in raw_blame:
        tmp.append(line)
        if not line:
            continue
        elif line[0] == "\t":
            blame.append("\n".join(tmp))
            tmp = list()

    return blame


def __raw_blame_to_blame(raw_blame: List[str]) -> List[Blame]:
    return list(filter(Blame.is_valid, map(Blame.of, raw_blame)))
