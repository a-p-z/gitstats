from dataclasses import dataclass

from gitstats.data.model.file import File


@dataclass(frozen=True)
class Diffstat:
    hash: str
    file: File
    insertions: int
    deletions: int
