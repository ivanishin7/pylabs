from __future__ import annotations

import functools
from typing import Callable, Generator, List


def fib_coroutine(
    func: Callable[..., Generator],
) -> Callable[..., Generator]:
    """Декоратор-прайминг: доводит сопрограмму до первого ``yield``."""

    @functools.wraps(func)
    def inner(*args: object, **kwargs: object) -> Generator:
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen

    return inner


@fib_coroutine
def fib_numbers() -> Generator[List[int], int, None]:
    """Сопрограмма: по числу ``n`` отдаёт первые ``n`` чисел ряда Фибоначчи."""
    result: List[int] = []
    while True:
        n: int = yield result
        result = []
        a, b = 0, 1
        for _ in range(n):
            result.append(a)
            a, b = b, a + b


if __name__ == "__main__":
    gen = fib_numbers()
    print(gen.send(3))
    print(gen.send(5))
    print(gen.send(8))
