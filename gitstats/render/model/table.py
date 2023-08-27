from typing import Any


class Table:
    __header: tuple[str, ...]
    __rows: Any

    def __init__(self, *args: str, **_):
        self.__header = args
        self.__rows = []

    def __getitem__(self, item: int) -> tuple[str | int | float | None, ...]:
        return self.__rows[item]

    @property
    def header(self) -> tuple[str, ...]:
        return self.__header

    @property
    def rows(self) -> list[tuple[str | int | float | None, ...]]:
        return self.__rows

    def add_row(self, *args: str | int | float | None, **_):
        self.__rows.append(args)

    def add_total_column(self):
        for i, row in enumerate(self.__rows):
            self.__rows[i] = row + (Table.__total_column(row),)

    def add_total_row(self):
        self.add_row(*Table.__total_row(self.__rows))

    def sort(
        self,
        column: int | None = None,
        key: Any = lambda row: row[0],
        reverse: bool = False,
    ):
        if column is not None:
            col: int = column
            self.__rows.sort(key=lambda row: row[col], reverse=reverse)
        elif key is not None:
            self.__rows.sort(key=key, reverse=reverse)

    def limit(self, value: int, others: bool = False):
        if len(self.__rows) <= value:
            return
        self.__rows, o = self.__rows[:value], self.__rows[value:]
        if others:
            self.__rows.append(Table.__total_row(o))

    @staticmethod
    def __total_row(rows: list[tuple[str | int | float | None, ...]]) -> tuple[str | int | float, ...]:
        total: list[int | float] = [0] * len(rows[0]) if len(rows) > 0 else []
        for row in rows:
            for i, e in enumerate(row):
                if isinstance(e, int) or isinstance(e, float):
                    total[i] += e
        return tuple(total)

    @staticmethod
    def __total_column(row: tuple[str | int | float, ...]) -> int | float:
        return sum([e for e in row if isinstance(e, int) or isinstance(e, float)])

    def is_not_empty(self) -> bool:
        return len(self.__rows) > 0

    def append(self, row: int, value: str | int | float):
        self.__rows[row] = self.__rows[row] + (value,)

    def update(self, row: int, col: int, value: str | int | float):
        t = list(self.__rows[row])
        t[col] = value
        self.__rows[row] = tuple(t)

    def fmt(self, fmt: str, row: int | None = None, col: int | None = None):
        rows = [row] if row is not None else range(len(self.__rows))
        for i in rows:
            t = list(self.__rows[i])
            cols = [col] if col is not None else range(len(t))
            for j in cols:
                t[j] = fmt % t[j]
            self.__rows[i] = tuple(t)
