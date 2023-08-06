#!/usr/bin/env python2

from fractions import Fraction

try:
    rational_types = (int, long, Fraction)
    range = xrange
except NameError:   # Python 3
    rational_types = (int, Fraction)


class Poly(dict):
    """The class defining a poly."""

    def __init__(self, coefficient=0, n=0):
        """Load up a poly instance."""
        # Na bazie Sedgewicka - tworzymy wielomian c*(x**n).
        # Wielomiany maja byc unormowane, bez zer przy wspolczynnikach.
        if coefficient != 0:
            self[n] = coefficient

    def is_zero(self):
        """Test if the poly is the zero polynomial."""
        # Pierwszy sposob dziala tez dla zerowych wspolczynnikow.
        # To jest szybkie, bo pierwszy niezerowy konczy petle.
        return all(self[k] == 0 for k in self)
        # Drugi sposob - gdy zer nie trzymamy.
        #return not self

    def degree(self):
        """Return the degree of the poly."""
        # Na razie pozwalam na zerowe wspolczynniki.
        if self.is_zero():
            return 0
        else:
            return max(k for k in self if self[k] != 0)

    key_deg = degree

    key_lex = degree

    key_deglex = degree

    def cancel(self):
        """Remove all zeros."""
        # Nie moge jednoczesnie iterowac i usuwac kluczy.
        to_delete = [k for k in self if self[k] == 0]
        for k in to_delete:
            del self[k]

    def __repr__(self):
        """Compute the string representation of the poly."""
        self.cancel()
        if self.is_zero():
            return "Poly()"
        else:
            L = list()
            for k in self:
                item = self[k]
                if isinstance(item, Fraction) and item.denominator == 1:
                    # Od razu upraszczamy. To wolno podczas iteracji.
                    item = item.numerator
                    self[k] = item
                if k == 0:
                    L.append("Poly({})".format(repr(item)))
                else:
                    L.append("Poly({}, {})".format(repr(item), k))
            return " + ".join(L)

    @classmethod
    def fromiterable(cls, data):
        """Create a poly from coefficients."""
        new_poly = cls()
        for (i, item) in enumerate(data):
            if item != 0:   # zer nie trzymamy
                new_poly[i] = item
        return new_poly

    def __getitem__(self, key):   # poly[k]
        """Return the coefficient."""
        # Mozemy pytac o dowolnie duzy wspolczynnik.
        return self.get(key, 0)

    def __add__(self, other):   # poly1 + poly2, poly + number, number + poly
        """Return the sum of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for k in self:
            new_poly[k] = new_poly.get(k, 0) + self[k]
        for k in other:
            new_poly[k] = new_poly.get(k, 0) + other[k]
        # To moze zwolnic kod.
        #new_poly.cancel()   # moze byc x + (-x) = 0
        return new_poly

    __radd__ = __add__

    def __sub__(self, other):       # poly1 - poly2
        """Return the difference of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for k in self:
            new_poly[k] = new_poly.get(k, 0) + self[k]
        for k in other:
            new_poly[k] = new_poly.get(k, 0) - other[k]
        # To moze zwolnic kod.
        #new_poly.cancel()   # moze byc x - x = 0
        return new_poly

    def __rsub__(self, other):       # poly1 - poly2
        """Return the difference of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for k in self:
            new_poly[k] = new_poly.get(k, 0) - self[k]
        for k in other:
            new_poly[k] = new_poly.get(k, 0) + other[k]
        # To moze zwolnic kod.
        #new_poly.cancel()
        return new_poly

    def __eq__(self, other):   # poly1 == poly2
        """Test if polys are equal."""
        return (self - other).is_zero()

    def __ne__(self, other):   # poly1 != poly2
        """Test if polys are not equal."""
        return not self == other

    def __mul__(self, other):        # poly1 * poly2
        """Return the product of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for i in self:
            for j in other:
                new_poly[i+j] = new_poly.get(i+j, 0) + self[i] * other[j]
        # To moze zwolnic kod.
        #new_poly.cancel()  # (x-2)*(x+2)=x**2-4, znika x**1
        return new_poly

    __rmul__ = __mul__

    def __pos__(self):
        """Return +poly."""
        return self

    def __neg__(self):
        """Return -poly."""
        new_poly = Poly()
        for k in self:
            new_poly[k] = -self[k]
        return new_poly

    def _eval1(self, x):   # schemat Hornera
        i = self.degree()
        result = self[i]   # istnieje
        while i > 0:
            i = i - 1
            result = result * x + self.get(i, 0)
        return result

    eval = _eval1

    def _combine1(self, other):  # zlozenie funkcji/wielomianow
        """Return the composition of two polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        i = self.degree()         # tez schemat Hornera
        new_poly = Poly(self[i])
        while i > 0:
            i = i - 1
            new_poly = new_poly * other + Poly(self.get(i, 0))
        #new_poly.cancel()   # niepotrzebne, bo jest w + i *
        return new_poly

    combine = _combine1

    def _power1(self, n):   # poly1 ** n
        new_poly = Poly(1)
        while n > 0:
            new_poly = new_poly * self
            n = n - 1
        #new_poly.cancel()   # niepotrzebne, bo jest w *
        return new_poly

    def _power2(self, n):     # poly1 ** n
        return Poly(1, n).combine(self)

    def _power3(self, n):       # poly1 ** n, binary
        if n < 0:
            raise ValueError("negative power")
        elif n == 0:
            return Poly(1)
        elif n == 1:
            return self
        elif n == 2:
            return self * self
        else:
            poly = self
            result = Poly(1)    # identycznosc w mnozeniu wielomianow
            while True:
                if n % 2 == 1:
                    result = result * poly
                    n = n - 1
                    if n == 0:
                        break
                if n % 2 == 0:
                    poly = poly * poly
                    n = n // 2
            #new_poly.cancel()   # niepotrzebne, bo jest w *
            return result

    __pow__ = _power3

    def diff(self):   # rozniczkowanie
        """Return the derivative of the poly."""
        # [c*x**n]' = c*n*x**(n-1)
        new_poly = Poly()
        for k in self:
            if k > 0:
                new_poly[k-1] = k * self[k]
        # Normowanie nie jest potrzebne.
        return new_poly

    def integrate(self):   # calkowanie
        """Return the integral of the poly."""
        # integrate(c*x**n, x) = c*x**(n+1)/(n+1) + const
        new_poly = Poly()
        for k in self:
            if isinstance(self[k], rational_types):
                new_poly[k+1] = self[k] * Fraction(1, k+1)
            else:
                new_poly[k+1] = self[k] / (k+1.0)
        # Normowanie nie jest potrzebne.
        return new_poly

    def __div__(self, other):        # poly / number, monomial / monomial
        """Dividing polys."""
        # Dopuszczamy dzielenie jednomianu przez jednomian.
        if isinstance(other, Poly):
            # Trzeba usunac zerowe wspolczynniki.
            self.cancel()
            other.cancel()
            if len(self) != 1 or len(other) != 1:
                raise ValueError("only monomials can be divided")
            k1 = list(self)[0]
            k2 = list(other)[0]
            if k1 < k2:
                raise ValueError("other is greater than self")
            coefficient1 = self[k1]
            coefficient2 = other[k2]
            if (isinstance(coefficient1, rational_types) and
                isinstance(coefficient2, rational_types)):   # AND
                    # Python 2.7: Fraction(Fraction, Fraction)
                    coefficient = Fraction(coefficient1, coefficient2)
            else:   # float, complex
                coefficient = coefficient1 / coefficient2
            return Poly(coefficient, k1 - k2)
        # Python 2.7: Fraction(Fraction, Fraction)
        elif isinstance(other, rational_types):
            return self * Poly(Fraction(1, other))
        else:
            return self * Poly(1.0 / other)

    __truediv__ = __div__

    def lcm(self, other):
        """Return the least common multiple of two monomials."""
        if not isinstance(other, Poly):
            other = Poly(other)
        self.cancel()
        other.cancel()
        if len(self) != 1 or len(other) != 1:
            raise ValueError("only monomials have lcm")
        k1 = list(self)[0]
        k2 = list(other)[0]
        return Poly(1, max(k1, k2))

    def __call__(self, x):
        if isinstance(x, Poly):
            return self.combine(x)
        else:
            return self.eval(x)

    def leading_term(self, key=None):
        """Return the leading term of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            k_max = key(self)
            return Poly(self[k_max], k_max)

    def leading_monomial(self, key=None):
        """Return the leading monomial of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            k_max = key(self)
            return Poly(1, k_max)

    def leading_coefficient(self, key=None):
        """Return the leading coefficient of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            k_max = key(self)
            return self[k_max]

    def iterterms(self):
        """The generator for terms from the poly."""
        self.cancel()   # remove zero terms
        for k in self:
            yield Poly(self[k], k)

# EOF
