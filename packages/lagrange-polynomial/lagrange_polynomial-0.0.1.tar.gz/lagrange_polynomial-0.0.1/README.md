# Lagrange Polynomials

Module to generate Lagrange polynomials over integers for 1-dimensional data.
This is generally useful for interpolation.

## Installation

Install with `pip`.

## Usage

### Example

```python
from lagrange_polynomial import LagrangePolynomial

xs = range(100)
ys = [f(x) for x in xs]          # For some function f

lp = LagrangePolynomial(xs, ys)  # Instantiate a polynomial with sequences of
                                 # x- and y-coordinates.

for x in xs:
    assert ys[x] == lp(x)        # Polynomial will intersect original points
    coefficient = lp.basis[0](x) # Get the 0th basis vector at x
```

### Interface

The `LagrangePolynomial` class takes two equally-sized sequences and an optional integer _p_.
The instance is a Lagrange polynomial _L_: _x_ -> _L_(_x_) over GF(_p_). If _p_ is not provided, it defaults to the 8<sup>th</sup> Mersenne prime _M_<sub>31</sub>.

It has a `basis` property, a `LagrangeBasis` object subclassing `Sequence`.
Each element _ℓⱼ_ indexed by integers _j_ in `range(len(xs))` is a function taking _x_ to its _j_<sup>th</sup> basis vector _ℓⱼ_(_x_).

## Test

Test with `make test`.
