#!/usr/bin/env python3

import itertools
from fractions import Fraction

try:
    rational_types = (int, long, Fraction)
    range = xrange
    from itertools import izip_longest as zip_longest
except NameError:   # Python 3
    rational_types = (int, Fraction)
    from itertools import zip_longest

class Poly(dict):
    """The class defining a poly."""

    def __init__(self, coefficient=0, *arguments):
        """Load up a poly instance."""
        # Tworzymy wielomian c*(x**n0)*(y**n1)*(z**n2)*...
        # Wielomiany maja byc unormowane, bez zer przy wspolczynnikach.
        if coefficient != 0 and arguments:   # normalizacja klucza
            new_key = list(arguments)
            while new_key[-1] == 0 and len(new_key) > 1:
                new_key.pop()
            self[tuple(new_key)] = coefficient
        elif coefficient != 0:
            self[(0,)] = coefficient

    def is_zero(self):
        """Test if the poly is the zero polynomial."""
        return all(self[key] == 0 for key in self) # moze beda zera, bezpieczne
        #return not self   # nie trzymamy zer

    def degree(self):
        """Return the degree of the poly."""
        if self.is_zero():
            return 0
        else:   # jest zabezpieczenie na zerowe wspolczynniki
            return max(sum(key) for key in self if self[key] != 0)

    def cancel(self):
        """Remove all zeros."""
        # Nie moge jednoczesnie iterowac i usuwac kluczy.
        to_delete = [key for key in self if self[key] == 0]
        for key in to_delete:
            del self[key]

    def __repr__(self):
        """Compute the string representation of the poly."""
        self.cancel()
        if self.is_zero():
            return "Poly()"
        else:
            L = list()
            key_list = list(self)
            key_list.sort()
            for key in key_list:
                item = self[key]
                if isinstance(item, Fraction) and item.denominator == 1:
                    # Od razu upraszczamy.
                    item = item.numerator
                    self[key] = item
                tmp = [repr(item)]
                tmp.extend(repr(i) for i in key)
                tmp = ", ".join(tmp)
                L.append("Poly({})".format(tmp))
            return " + ".join(L)

    @classmethod
    def fromiterable(cls, data):
        """Create a poly from a list of coefficients."""
        new_poly = cls()
        for (i, coefficient) in enumerate(data): # wielomian jednej zmiennej
            if coefficient != 0:   # zer nie trzymamy
                new_poly += cls(coefficient, i)
        return new_poly

    def __getitem__(self, key):   # poly[key]
        """Return the coefficient."""
        # Mozemy pytac o dowolny wspolczynnik.
        # user moze podac int zamiast tuple.
        if not isinstance(key, tuple):
            key = (key,)
        # Normujemy klucz.
        new_key = list(key)
        while new_key[-1] == 0 and len(new_key) > 1:
            new_key.pop()
        return self.get(tuple(new_key), 0)

    def __add__(self, other):      # poly1 + poly2
        """Return the sum of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for key in self:
            new_poly[key] = new_poly.get(key, 0) + self[key]
        for key in other:
            new_poly[key] = new_poly.get(key, 0) + other[key]
        new_poly.cancel()
        return new_poly

    __radd__ = __add__

    def __sub__(self, other):       # poly1 - poly2
        """Return the difference of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for key in self:
            new_poly[key] = new_poly.get(key, 0) + self[key]
        for key in other:
            new_poly[key] = new_poly.get(key, 0) - other[key]
        new_poly.cancel()
        return new_poly

    def __rsub__(self, other):       # poly1 - poly2
        """Return the difference of polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for key in self:
            new_poly[key] = new_poly.get(key, 0) - self[key]
        for key in other:
            new_poly[key] = new_poly.get(key, 0) + other[key]
        new_poly.cancel()
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
        for key1 in self:
            for key2 in other:
                new_key = [x + y for (x, y) in zip_longest(key1, key2, fillvalue=0)]
                new_key = tuple(new_key)
                new_poly[new_key] = ( new_poly.get(new_key, 0) 
                    + self[key1] * other[key2] )
        new_poly.cancel()   # (x-2)*(x+2)=x**2-4, znika x**1
        return new_poly

    __rmul__ = __mul__

    def __pos__(self):
        """Return +poly."""
        return self

    def __neg__(self):
        """Return -poly."""
        new_poly = Poly()
        for key in self:
            new_poly[key] = -self[key]
        return new_poly

    def _power1(self, n):   # poly**n
        new_poly = Poly(1)
        while n > 0:
            new_poly *= self
            n = n - 1
        return new_poly

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
                    result *= poly
                    n = n - 1
                    if n == 0:
                        break
                if n % 2 == 0:
                    poly = poly * poly
                    n = n // 2
            #new_poly.cancel()   # niepotrzebne, bo jest w *
            return result

    __pow__ = _power3

    def __div__(self, other):        # poly / number, monomial / monomial
        """Dividing polys."""
        # Dopuszczamy dzielenie jednomianu przez jednomian.
        if isinstance(other, Poly):
            # Trzeba usunac zerowe wspolczynniki, jezeli byly dopuszczone.
            #self.cancel()
            #other.cancel()
            if len(self) != 1 or len(other) != 1:
                raise ValueError("only monomials can be divided")
            key1 = list(self)[0]
            key2 = list(other)[0]
            new_key = [x - y for (x, y) in
                zip_longest(key1, key2, fillvalue=0)]
            if any(item < 0 for item in new_key):
                raise ValueError("other is greater than self")
            # Normujemy klucz. Przyklad:
            # Poly(1,2,1) / Poly(1,1,1) = Poly(1,1), klucz (1,), a nie (1, 0).
            while new_key[-1] == 0 and len(new_key) > 1:
                new_key.pop()
            new_key = tuple(new_key)
            coefficient1 = self[key1]
            coefficient2 = other[key2]
            if (isinstance(coefficient1, rational_types) and
                isinstance(coefficient2, rational_types)):   # AND
                    # Python 2.7: Fraction(Fraction, Fraction)
                    coefficient = Fraction(coefficient1, coefficient2)
            else:   # float, complex
                coefficient = coefficient1 / coefficient2
            return Poly(coefficient, *new_key)
        elif isinstance(other, rational_types):
            # Python 2.7: Fraction(Fraction, Fraction)
            return self * Poly(Fraction(1, other))
        else:
            return self * Poly(1.0 / other)

    __truediv__ = __div__

    def lcm(self, other):
        """Return the least common multiple of two monomials."""
        if not isinstance(other, Poly):
            other = Poly(other)
        # Jezeli dopuszczamy zera, to trzeba upraszczac.
        #self.cancel()
        #other.cancel()
        if len(self) != 1 or len(other) != 1:
            raise ValueError("only monomials have lcm")
        key1 = list(self)[0]
        key2 = list(other)[0]
        new_key = [max(x, y) for (x, y) in
            zip_longest(key1, key2, fillvalue=0)]
        new_key = tuple(new_key)
        return Poly(1, *new_key)

    def diff(self, var=0):   # rozniczkowanie
        """Return the derivative of the poly."""
        # [c*x**n]' = c*n*x**(n-1)
        new_poly = Poly()
        for key in self:
            if var > len(key)-1 or key[var] == 0:
                continue   # nie ma tej zmiennej w wyrazie
            coefficient = self[key] * key[var]
            new_key = list(key)
            new_key[var] -= 1
            # Normujemy klucz. Przyklad:
            # Poly(1,0,1).diff(1)=1, klucz (0,), a nie (0, 0).
            while new_key[-1] == 0 and len(new_key) > 1:
                new_key.pop()
            new_key = tuple(new_key)
            new_poly[new_key] = coefficient
        return new_poly

    def integrate(self, var=0):   # calkowanie
        """Return the integral of the poly."""
        # integrate(c*x**n, x) = c*x**(n+1)/(n+1) + const
        new_poly = Poly()
        for key in self:
            coefficient = self[key]
            # Trzeba dobrac dlugosc nowego klucza.
            new_key = [0] * max(len(key), var+1)
            # Odtwarzamy stare wartosci klucza.
            for i, item in enumerate(key):
                new_key[i] += item
            if isinstance(coefficient, rational_types):
                coefficient *= Fraction(1, new_key[var] + 1)
            else:
                coefficient /= new_key[var] + 1.0
            # Teraz pojawia sie nowa wartosc klucza.
            new_key[var] += 1
            new_key = tuple(new_key)
            new_poly[new_key] = coefficient
        return new_poly

    def _combine1(self, other, var=0):  # zlozenie wielomianow
        """Return the composition of two polys."""
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        for key in self:
            coefficient = self[key]
            if var > len(key)-1 or key[var] == 0:
                # Dodajemy wyraz bez zmian.
                new_poly += Poly(coefficient, *key)
                continue
            new_key = list(key)
            new_key[var] = 0   # znika dana zmienna
            new_key = tuple(new_key)
            new_poly += Poly(coefficient, *new_key) * pow(other, key[var])
            # Normowanie jest zawarte w + i *.
        return new_poly

    def _combine2(self, other, var=0):  # zlozenie wielomianow
        """Return the composition of two polys."""
        # Optymalizacja przez przechowywanie juz obliczonych poteg.
        if not isinstance(other, Poly):
            other = Poly(other)
        new_poly = Poly()
        powers = dict()
        for key in self:
            coefficient = self[key]
            if var > len(key)-1 or key[var] == 0:
                # Dodajemy wyraz bez zmian.
                new_poly += Poly(coefficient, *key)
                continue
            new_key = list(key)
            new_key[var] = 0   # znika dana zmienna
            new_key = tuple(new_key)
            if key[var] not in powers:
                powers[key[var]] = pow(other, key[var])
            new_poly += Poly(coefficient, *new_key) * powers[key[var]]
            # Normowanie jest zawarte w + i *.
        return new_poly

    combine = _combine2

    def key_lex(self):
        """The sorting key for lexicographic order."""
        alist = max([0] + list(key) for key in self)
        return tuple(alist)

    def key_deglex(self):
        """The sorting key for graded lexicographic order."""
        alist = max([sum(key)] + list(key) for key in self)
        return tuple(alist)

    key_deg = key_deglex

    def leading_term(self, key=None):
        """Return the leading term of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            new_key = key(self)
            new_key = tuple(new_key[1:])
            return Poly(self[new_key], *new_key)

    def leading_monomial(self, key=None):
        """Return the leading monomial of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            new_key = key(self)
            new_key = tuple(new_key[1:])
            return Poly(1, *new_key)

    def leading_coefficient(self, key=None):
        """Return the leading coefficient of the poly."""
        if self.is_zero():
            raise ValueError("zero poly")
        else:
            new_key = key(self)
            new_key = tuple(new_key[1:])
            return self[new_key]

    def iterterms(self):
        """The generator for terms from the poly."""
        self.cancel()   # remove zero terms
        for key in self:
            yield Poly(self[key], *key)

# EOF
