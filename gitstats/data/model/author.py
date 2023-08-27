from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from functools import total_ordering


@dataclass(frozen=True)
@total_ordering
class Author:
    name: str
    email: str
    start: datetime = datetime.now(tz=UTC)
    end: datetime = datetime.now(tz=UTC)
    username: str | None = None

    def is_dead(self) -> bool:
        return (datetime.now(tz=UTC) - self.end).days > 365

    def __repr__(self) -> str:
        return self.name

    def __lt__(self, other: "Author") -> bool:
        return self.name < other.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Author):
            return self.email == other.email
        return False

    def __hash__(self):
        return hash(self.email)


Committer = Author
Reviewer = Author
