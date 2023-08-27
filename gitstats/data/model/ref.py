from dataclasses import dataclass
from datetime import datetime

from gitstats.data.model.author import Author


@dataclass(frozen=True)
class Ref:
    name: str
    author: Author
    date: datetime
