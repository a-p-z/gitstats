import logging
import pickle
from typing import List

from core.mailmap import Mailmap
from core.model.blame import Blame
from core.model.numstat import Numstat


def load_numstat() -> List[Numstat]:
    Mailmap.instance().authors_by_email = __load("authors_by_email.pkl")
    return __load("numstat.pkl")


def load_blame() -> List[Blame]:
    return __load("blame.pkl")


def dump_numstat(numstat: List[Numstat]):
    __dump(numstat, "numstat.pkl")
    __dump(Mailmap.instance().authors_by_email, "authors_by_email.pkl")


def dump_blame(blame: List[Blame]):
    __dump(blame, "blame.pkl")


def __load(file: str):
    # TODO ignore file too old
    with open(file, "rb") as _input:
        _object = pickle.load(_input)
        logging.info("loaded %s", file)
        return _object


def __dump(_object, file: str):
    # TODO overwrite existing
    with open(file, "wb") as output:
        pickle.dump(_object, output, pickle.HIGHEST_PROTOCOL)
