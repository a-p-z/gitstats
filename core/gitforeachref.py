import logging
from datetime import datetime
from typing import List, Dict

from core import process
from core.mailmap import Mailmap

GIT_FOR_EACH_REF = "git for-each-ref" \
                   " --format='%(committerdate:iso8601).:*-*:.%(authorname).:*-*:.%(authoremail).:*-*:.%(refname)'" \
                   " refs/remotes/origin"


def git_refs_remotes_origin() -> List[List]:
    """
    :return: list of [date, author, ref]
    """
    logging.info("executing %s", GIT_FOR_EACH_REF)
    lines = process.execute(GIT_FOR_EACH_REF).split("\n")[:-1]
    return list(map(raw_line_to_ref, lines))


def raw_line_to_ref(line: str) -> List:
    raw_ref = line.split(".:*-*:.")
    date = datetime.strptime(raw_ref[0], "%Y-%m-%d %H:%M:%S %z")
    name = raw_ref[1]
    email = raw_ref[2][1:-1]
    branch = raw_ref[3]
    author = Mailmap.get_or_default(name, email)
    return [date, author, branch]
