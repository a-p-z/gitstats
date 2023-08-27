from dataclasses import dataclass


@dataclass(frozen=True)
class CommitsAndImpact:
    commits: int
    insertions: int
    deletions: int
    merges: int = 0
    total_impact: int = 0  # insertions + deletions of all the commits
    eloc: int = 0  # edited line of code

    @property
    def impact_over_commit(self) -> float:
        return (self.insertions + self.deletions) / self.commits if self.commits != 0 else 0

    @property
    def deletion_ratio(self) -> float:
        return self.deletions / self.commits if self.commits != 0 else 0

    @property
    def percentage_of_changes(self) -> float:
        return 100.0 * (self.insertions + self.deletions) / self.total_impact if self.total_impact != 0 else 0

    @property
    def stability(self) -> float:
        return 100 * self.eloc / self.insertions if self.insertions != 0 else 0

    def __add__(self, other: "CommitsAndImpact") -> "CommitsAndImpact":
        return CommitsAndImpact(
            self.commits + other.commits,
            self.insertions + other.insertions,
            self.deletions + other.deletions,
            self.merges + other.merges,
            self.total_impact + other.total_impact,
            self.eloc + other.eloc,
        )
