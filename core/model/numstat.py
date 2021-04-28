from datetime import datetime

from core.model.author import Author
from core.model.commit import Commit
from core.model.diffstat import Diffstat


class Numstat:

    def __init__(self,
                 _hash: str,
                 date: datetime,
                 subject: str,
                 author: Author,
                 committer: Author,
                 file: str,
                 insertions: int,
                 deletions: int):
        self.hash = _hash
        self.date = date
        self.subject = subject
        self.author = author
        self.committer = committer
        self.file = file
        self.insertions = insertions
        self.deletions = deletions

    def __getitem__(self, item):
        return getattr(self, item)

    @staticmethod
    def of(commit: Commit, diffstat: Diffstat):
        return Numstat(commit.hash,
                       commit.date,
                       commit.subject,
                       commit.author,
                       commit.committer,
                       diffstat.file,
                       diffstat.insertions,
                       diffstat.deletions)
