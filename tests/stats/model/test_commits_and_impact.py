from gitstats.stats.model.commits_and_impact import CommitsAndImpact


def test_impact_over_commit():
    commits_and_impact = CommitsAndImpact(123, 2632, 2534)
    assert commits_and_impact.impact_over_commit == 42


def test_impact_over_commit_with_zero_commits():
    commits_and_impact = CommitsAndImpact(0, 2632, 2534)
    assert commits_and_impact.impact_over_commit == 0


def test_deletion_ratio():
    commits_and_impact = CommitsAndImpact(123, 6126, 5166)
    assert commits_and_impact.deletion_ratio == 42


def test_deletion_ratio_with_zero_commits():
    commits_and_impact = CommitsAndImpact(6126, 5166, 0)
    assert commits_and_impact.deletion_ratio == 0


def test_percentage_of_changes():
    commits_and_impact = CommitsAndImpact(123, 2101, 2099, total_impact=10000)
    assert commits_and_impact.percentage_of_changes == 42


def test_percentage_of_changes_with_zero_total_impact():
    commits_and_impact = CommitsAndImpact(2101, 2099, 123, total_impact=0)
    assert commits_and_impact.percentage_of_changes == 0


def test_stability():
    commits_and_impact = CommitsAndImpact(1234, 12300, 11099, eloc=5166)
    assert commits_and_impact.stability == 42


def test_stability_with_zero_insertions():
    commits_and_impact = CommitsAndImpact(0, 0, 0, eloc=123)
    assert commits_and_impact.stability == 0


def test_add():
    a = CommitsAndImpact(22, 21, 20, 19, 18, 17)
    b = CommitsAndImpact(20, 21, 22, 23, 24, 25)
    c = CommitsAndImpact(42, 42, 42, 42, 42, 42)
    assert a + b == c
