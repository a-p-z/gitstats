from dataclasses import dataclass
from datetime import datetime

from gitstats.data.model.author import Author
from gitstats.data.model.author import Committer
from gitstats.data.model.file import File


@dataclass(frozen=True)
class Numstat:
    hash: str
    parent: str
    date: datetime
    subject: str
    author: Author
    committer: Committer
    file: File | None = None
    insertions: int = 0
    deletions: int = 0

    @property
    def impact(self) -> int:
        return self.insertions + self.deletions

    def is_merge(self):
        return self.parent and " " in self.parent

    def is_commit(self) -> bool:
        return not self.is_merge()
