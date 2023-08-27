from dataclasses import dataclass

from gitstats.data.model.author import Author


@dataclass(frozen=True)
class ShortLog:
    author: Author
    commits: int
