from typing import List

from core.mailmap import Mailmap
from core.model.author import Author
from datetime import datetime
from core.model.diffstat import Diffstat


class Commit:

    def __init__(self,
                 _hash: str,
                 subject: str,
                 author: Author,
                 committer: Author,
                 date: datetime,
                 diffstats: List[Diffstat],
                 email: str = "EMAIL PLACEHOLDER"
                 ):
        self.hash = _hash
        self.subject = subject
        self.author = author
        self.email = email
        self.committer = committer
        self.date = date
        self.diffstats = diffstats

    @staticmethod
    def of(log: str):
        log_list = log.split("\n")
        _hash = log_list[0]
        subject = log_list[2]
        date = datetime.strptime(log_list[1][:-6], "%Y-%m-%dT%H:%M:%S")
        author = Mailmap.instance().get(log_list[3], log_list[4], date)
        committer = Mailmap.instance().get(log_list[5], log_list[6])
        diffstats = [Diffstat.of(diffstat) for diffstat in log_list[8:-1]]
        return Commit(_hash, subject, author, committer, date, diffstats, email=log_list[4])

    def __hash__(self):
        return self.hash

    def sum_deletions(self):
        return sum([diffstat.deletions for diffstat in self.diffstats])

    def sum_insertions(self):
        return sum([diffstat.insertions for diffstat in self.diffstats])

    def impacted_filenames(self):
        return [diffstat.file for diffstat in self.diffstats]

    def sum_impacts(self):
        return self.sum_insertions() + self.sum_deletions()
