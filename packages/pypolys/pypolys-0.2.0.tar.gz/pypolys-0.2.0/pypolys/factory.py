#!/usr/bin/env python3

import random
from fractions import Fraction


class PolyFactory:
    """The class for poly generators."""

    def __init__(self, poly_class):
        """Get a poly class."""
        self.cls = poly_class
        self.HERMITE = {0: self.cls(1), 1: self.cls(2, 1)}
        self.CHEBYSHEV = {0: self.cls(1), 1: self.cls(1, 1)}
        self.LEGENDRE = {0: self.cls(1), 1: self.cls(1, 1)}

    def natural(self, n=1):
        """Create a poly (x-1)*(x-2)*...*(x-n)."""
        poly = self.cls(1)
        for i in range(1, n+1):
            poly = poly * (self.cls(1, 1) -i)
        return poly

    def geometric(self, n=1):
        """Create a poly 1 + x + x**2 + ... + x**n."""
        poly = self.cls(1)
        for i in range(1, n+1):
            poly = poly + self.cls(1, i)
        return poly

    def hermite(self, n=1):
        """Create a Hermite polynomial."""
        if n not in self.HERMITE:
            self.HERMITE[n] = (self.cls(2, 1) * self.hermite(n-1) 
                            + self.cls(2*n-2) * self.hermite(n-2))
        return self.HERMITE[n]

    def chebyshev(self, n=1):
        """Create a Chebyshev polynomial."""
        if n not in self.CHEBYSHEV:
            self.CHEBYSHEV[n] = (self.cls(2, 1) * self.chebyshev(n-1) 
                                 + self.cls(-1) * self.chebyshev(n-2))
        return self.CHEBYSHEV[n]

    def legendre(self, n=1):
        """Create a Legendre polynomial."""
        if n not in self.LEGENDRE:
            self.LEGENDRE[n] = (
                self.cls(Fraction(2*n-1, n), 1) * self.legendre(n-1) 
                   + self.cls(Fraction(-n+1, n)) * self.legendre(n-2))
        return self.LEGENDRE[n]

# EOF
