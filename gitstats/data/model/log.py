from dataclasses import dataclass
from datetime import datetime

from gitstats.data.model.author import Author
from gitstats.data.model.author import Committer
from gitstats.data.model.diffstat import Diffstat


@dataclass(frozen=True)
class Log:
    hash: str
    parent: str
    date: datetime
    subject: str
    author: Author
    committer: Committer
    diffstats: list[Diffstat]

    def is_merge(self) -> bool:
        return bool(self.parent) and " " in self.parent

    def is_commit(self) -> bool:
        return not self.is_merge()

    @property
    def insertions(self) -> int:
        return sum([ds.insertions for ds in self.diffstats])

    @property
    def deletions(self) -> int:
        return sum([ds.deletions for ds in self.diffstats])

    @property
    def impact(self) -> int:
        return self.insertions + self.deletions
