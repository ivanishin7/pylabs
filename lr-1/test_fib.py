"""Тесты (unittest) для итераторов и сопрограммы ряда Фибоначчи."""
import unittest

from fib_coroutine import fib_numbers
from fib_iterator import FibGetItem, FibIterator

EXPECTED = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


class TestFibGetItem(unittest.TestCase):
    """Итератор через ``__getitem__`` (упрощённый способ)."""

    def test_normal(self) -> None:
        """Перебор выдаёт первые ``count`` чисел ряда."""
        self.assertEqual(list(FibGetItem(10)), EXPECTED)

    def test_indexing(self) -> None:
        """Доступ по индексу возвращает n-й элемент ряда."""
        self.assertEqual(FibGetItem(10)[6], 8)

    def test_empty(self) -> None:
        """Краевой случай: ноль элементов даёт пустой список."""
        self.assertEqual(list(FibGetItem(0)), [])

    def test_single(self) -> None:
        """Краевой случай: один элемент."""
        self.assertEqual(list(FibGetItem(1)), [0])

    def test_out_of_range(self) -> None:
        """Выход за диапазон возбуждает IndexError."""
        with self.assertRaises(IndexError):
            FibGetItem(3)[3]


class TestFibIterator(unittest.TestCase):
    """Итератор через ``__iter__`` / ``__next__`` (обычный способ)."""

    def test_normal(self) -> None:
        """Перебор выдаёт первые ``count`` чисел ряда."""
        self.assertEqual(list(FibIterator(10)), EXPECTED)

    def test_empty(self) -> None:
        """Краевой случай: ноль элементов."""
        self.assertEqual(list(FibIterator(0)), [])

    def test_single(self) -> None:
        """Краевой случай: один элемент."""
        self.assertEqual(list(FibIterator(1)), [0])

    def test_stop_iteration(self) -> None:
        """После исчерпания возбуждается StopIteration."""
        it = FibIterator(1)
        next(it)
        with self.assertRaises(StopIteration):
            next(it)


class TestFibCoroutine(unittest.TestCase):
    """Сопрограмма, возвращающая список чисел ряда по ``send(n)``."""

    def test_send_3(self) -> None:
        """Тривиальный случай n = 3."""
        gen = fib_numbers()
        self.assertEqual(gen.send(3), [0, 1, 1])

    def test_send_5(self) -> None:
        """Пять первых членов ряда."""
        gen = fib_numbers()
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])

    def test_multiple_sends(self) -> None:
        """Один экземпляр корректно обрабатывает несколько send подряд."""
        gen = fib_numbers()
        self.assertEqual(gen.send(3), [0, 1, 1])
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])
        self.assertEqual(gen.send(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_send_zero(self) -> None:
        """Краевой случай: n = 0 даёт пустой список."""
        gen = fib_numbers()
        self.assertEqual(gen.send(0), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
