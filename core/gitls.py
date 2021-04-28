import logging
from typing import List

from core import process

GIT_LS_FILES = "git ls-files"


def git_ls_files() -> List[str]:
    logging.info("executing %s", GIT_LS_FILES)
    return process.execute(GIT_LS_FILES).split("\n")[0:-1]
