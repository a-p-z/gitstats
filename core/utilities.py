from collections import defaultdict
from numbers import Number
from typing import List, Any, Dict

from core.model.author import Author


def limit(table: List[List], _limit: int, other=False) -> List[List]:
    if len(table) <= _limit:
        return table

    if not other:
        return table[:_limit]

    a = table[:_limit - 1]
    b = sum_by_row(table[_limit - 1:])
    b[0] = "others"
    return a + [b]


def sum_by_row(table: List[List]) -> List:
    total = [0] * len(table[0])
    for i in range(len(table)):
        for j in range(len(total)):
            if isinstance(table[i][j], Number):
                total[j] += table[i][j]
    return total


def sum_by_column(table: List[List]):
    for i in range(len(table)):
        table[i].append(sum(filter(lambda x: isinstance(x, Number), table[i])))


def cumulate_rows(table: List[List]):
    for i in range(1, len(table)):
        for j in range(1, len(table[i])):
            table[i][j] += table[i - 1][j]


def group_rows_by_year(table: List[List]) -> List[List]:
    result = defaultdict(lambda: [0] * len(table[0]))
    for i in range(0, len(table)):
        year = table[i][0][:4]
        result[year][0] = year
        for j in range(1, len(table[i])):
            result[year][j] += table[i][j]
    return list(result.values())


def add_percentage_of_changes_column(table: List[List], insertions_index: int, deletions_index: int) -> List[List]:
    """
    :param insertions_index: index for insertions
    :param deletions_index: index for deletions
    :param table:
    :return: % of changes = 100 * (insertions + deletions) / (total_insertions + total_deletions)
    """
    # TODO
    total_insertions_deletions = sum(map(lambda x: x[insertions_index] + x[deletions_index], table))
    return list(
        map(lambda x: x + [
            float("{:.2f}".format((100.0 * (x[insertions_index] + x[deletions_index]) / total_insertions_deletions)))],
            table))


def add_impact_commit_column(table: List[List],
                             insertions_index: int,
                             deletions_index: int,
                             commits_index: int) -> List[List]:
    """
    :param insertions_index: index for insertions
    :param deletions_index: index for deletions
    :param commits_index: index for commits
    :param table:
    :return: impact/commit = (insertions + deletions) / commits
    """
    # TODO
    return list(map(lambda x: x + [int((x[insertions_index] + x[deletions_index]) / x[commits_index])], table))


def add_star(table: List[List], i: int = 0, j: int = 0) -> str:
    # TODO
    return str(table[i][j]) + " (*y)"


def replace_author_row(table: List) -> List[str]:
    # TODO apply_to_row
    result = list()
    for i in range(len(table)):
        result.append(table[i].name if isinstance(table[i], Author) else table[i])
    return result


def replace_author_column(table: List[List], column: int = 0):
    # TODO apply_to_column
    for row in range(len(table)):
        table[row][column] = table[row][column].name if isinstance(table[row][column], Author) else table[row][column]


def first_column(table):
    return table[0]


def second_column(table):
    return table[1]


def aggregate_and_sum(items: List[Any], attr_to_aggregate: str, attr_to_sum: str) -> Dict[Any, int]:
    sum_by_attr = defaultdict(int)
    for item in items:
        sum_by_attr[item[attr_to_aggregate]] += item[attr_to_sum]
    return sum_by_attr


def apply_to_column(table: List[List], column, f):
    for row in table:
        row[column] = f(row[column])


def apply_to_row(table: List[List], row, f):
    for column in range(len(table[row])):
        table[row][column] = f(table[row][column])


def filter_active_authors(header: List, data):
    for i in range(len(header) - 1, 0, -1):
        if not header[i].is_active():
            del header[i]
            for j in range(len(data)):
                del data[j][i]
    return header, data
