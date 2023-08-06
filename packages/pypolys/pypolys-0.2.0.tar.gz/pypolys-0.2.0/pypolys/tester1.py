#!/usr/bin/env python3

import unittest
import random
from fractions import Fraction
from pypolys.polys import Poly

x = Poly(1, 1)
p = (x-1) * (x+1) +1
print(p)   # tu jest p.cancel() w __repr__
print(len(p))   # ogolnie moga byc zerowe wspolczynniki
assert (p / x) == x   # trzeba usunac zerowe wspolczynniki

# EOF
