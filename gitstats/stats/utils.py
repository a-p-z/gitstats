from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

K = TypeVar("K")
K1 = TypeVar("K1")
K2 = TypeVar("K2")
T1 = TypeVar("T1")
T2 = TypeVar("T2")


def group_by(items: list[T1], fk: Callable[[T1], K], fv: Callable[[list[T1]], T2]) -> dict[K, T2]:
    grouped = defaultdict(list)
    for item in items:
        grouped[fk(item)].append(item)
    return {k: fv(items) for k, items in grouped.items()}


def group_by_by(
    items: list[T1],
    fk1: Callable[[T1], K1],
    fk2: Callable[[T1], K2],
    fv: Callable[[list[T1]], T2],
) -> dict[K1, dict[K2, T2]]:
    grouped: dict[K1, dict[K2, list[T1]]] = defaultdict(lambda: defaultdict(list))
    for item in items:
        grouped[fk1(item)][fk2(item)].append(item)
    return {k1: {k2: fv(items) for k2, items in grouped_items.items()} for k1, grouped_items in grouped.items()}
