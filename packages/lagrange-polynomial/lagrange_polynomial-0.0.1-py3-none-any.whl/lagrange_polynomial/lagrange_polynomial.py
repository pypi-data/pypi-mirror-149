#!/usr/bin/env python3
"""Lagrange polynomial"""

from functools import partial
from collections.abc import Sequence
from typing import Callable, Union, overload

Polynomial = Callable[[int], int]

class LagrangeBasis(Sequence[Polynomial]):
    """Factory class for Lagrange basis polynomials"""

    def __init__(self, x_points: Sequence[int], prime: int) -> None:
        self.xs = x_points
        self.prime = prime
        self._index = 0

    def __iter__(self) -> "LagrangeBasis":
        return self

    def __next__(self) -> Polynomial:
        if self._index < len(self):
            self._index += 1
            return self[self._index -1]
        raise StopIteration

    def __len__(self) -> int:
        return len(self.xs)

    @overload
    def __getitem__(self, key: int) -> Polynomial:
        pass

    @overload
    def __getitem__(self, key: slice) -> list[Polynomial]:
        pass

    def __getitem__(self, key: Union[int, slice]) -> Union[Polynomial,
                                                           list[Polynomial]]:
        if isinstance(key, int):
            return partial(self._basis, key)

        step = key.step or 1
        start = key.start or 0
        return [partial(self._basis, j) \
                for j in range(start, key.stop, step)]

    def _basis(self, j: int, x: int) -> int:
        """Lagrange basis polynomial ℓ_j(x)"""
        x_j = self.xs[j]
        product = 1.0
        for m, x_m in enumerate(self.xs):
            if m != j:
                product *= (x - x_m) / (x_j - x_m)
                product %= self.prime
        return int(product)

class LagrangePolynomial:
    """Lagrange polynomial function"""

    def __init__(self, x_points: Sequence[int],
                 y_points: Sequence[int], prime: int = None) -> None:
        self.xs = x_points
        self.ys = y_points

        if len(self.xs) != len(self.ys):
            raise RuntimeError("The number of x- and y-coordinates must be equal")
        if len(self.xs) != len(set(self.xs)):
            raise RuntimeError("All x-coordinates must be unique")

        self.prime = prime or 2 ** 31 - 1
        self.basis = LagrangeBasis(self.xs, self.prime)

    def __repr__(self) -> str:
        return f"LagrangePolynomial(xs, ys, {self.prime})"

    def __call__(self, x: int) -> int:
        return self._lagrange_poly(x)

    def _lagrange_poly(self, x: int) -> int:
        """Lagrange polynomial at x"""
        total = 0
        for j, y in enumerate(self.ys):
            total += y * self.basis[j](x)
        return total % self.prime

def main() -> None:
    """Entry point"""
    xs = range(1, 6)
    ys = [x ** 3 for x in xs]

    lp = LagrangePolynomial(xs, ys, 17)

    for x, y in zip(xs, ys):
        print(x, y, y % lp.prime, lp(x))
        assert y % lp.prime == lp(x)

    print(lp(0))

if __name__ == "__main__":
    main()
