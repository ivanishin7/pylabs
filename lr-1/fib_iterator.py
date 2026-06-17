from __future__ import annotations


class FibGetItem:
    """Упрощённый итерируемый объект на основе одного метода ``__getitem__``."""

    def __init__(self, count: int) -> None:
        """Запомнить количество выдаваемых элементов ряда."""
        self.count: int = count

    def __getitem__(self, index: int) -> int:
        """Вернуть ``index``-й элемент ряда; ``IndexError`` завершает перебор."""
        if index < 0 or index >= self.count:
            raise IndexError("индекс вне диапазона ряда Фибоначчи")
        a, b = 0, 1
        for _ in range(index):
            a, b = b, a + b
        return a


class FibIterator:
    """«Обычный» итератор на основе методов ``__iter__`` и ``__next__``."""

    def __init__(self, count: int) -> None:
        """Инициализировать счётчик и начальные значения ряда."""
        self.count: int = count
        self._idx: int = 0
        self._a: int = 0
        self._b: int = 1

    def __iter__(self) -> "FibIterator":
        """Вернуть сам объект — он же является итератором."""
        return self

    def __next__(self) -> int:
        """Вернуть очередное число ряда; ``StopIteration`` по исчерпании."""
        if self._idx >= self.count:
            raise StopIteration
        self._idx += 1
        value = self._a
        self._a, self._b = self._b, self._a + self._b
        return value


if __name__ == "__main__":
    print(list(FibGetItem(10)))
    print(list(FibIterator(10)))
