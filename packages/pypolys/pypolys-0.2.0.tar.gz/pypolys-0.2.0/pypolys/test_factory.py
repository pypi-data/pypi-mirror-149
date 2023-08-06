#!/usr/bin/env python3

import unittest
import math
from fractions import Fraction
from pypolys.polys import Poly
#from pypolys.mpolys import Poly
from pypolys.factory import PolyFactory


class TestPolyFactory(unittest.TestCase):

    def setUp(self):
        self.N = 10
        self.poly_factory = PolyFactory(Poly)

    def test_natural(self):
        p = self.poly_factory.natural(n=self.N)
        #print(p)
        self.assertEqual(p.degree(), self.N)
        self.assertEqual(p[self.N], 1)
        self.assertEqual(p[self.N-1], sum(-i for i in range(self.N+1)))
        self.assertEqual(p[0], math.factorial(self.N))

    def test_geometric(self):
        p = self.poly_factory.geometric(n=self.N)
        #print(p)
        self.assertEqual(p.degree(), self.N)
        for i in range(self.N+1):
            self.assertEqual(p[i], 1)

    def test_hermite(self):
        p = self.poly_factory.hermite(n=self.N)
        #print p
        #print self.poly_factory.HERMITE   # sa wszystkie
        self.assertEqual(p.degree(), self.N)
        h0 = self.poly_factory.hermite(n=0)
        h1 = self.poly_factory.hermite(n=1)
        h2 = self.poly_factory.hermite(n=2)
        h3 = self.poly_factory.hermite(n=3)
        h4 = self.poly_factory.hermite(n=4)
        h5 = self.poly_factory.hermite(n=5)
        self.assertEqual(h0, Poly(1))
        self.assertEqual(h1, Poly(2, 1))
        self.assertEqual(h2, Poly(2) + Poly(4, 2))
        self.assertEqual(h3, Poly(12, 1) + Poly(8, 3))
        self.assertEqual(h4, Poly(12) + Poly(48, 2) + Poly(16, 4))
        self.assertEqual(h5, Poly(120, 1) + Poly(160, 3) + Poly(32, 5))

    def test_chebyshev(self):
        p = self.poly_factory.chebyshev(n=self.N)
        #print p
        #print self.poly_factory.CHEBYSHEV   # sa wszystkie
        self.assertEqual(p.degree(), self.N)
        t0 = self.poly_factory.chebyshev(n=0)
        t1 = self.poly_factory.chebyshev(n=1)
        t2 = self.poly_factory.chebyshev(n=2)
        t3 = self.poly_factory.chebyshev(n=3)
        t4 = self.poly_factory.chebyshev(n=4)
        t5 = self.poly_factory.chebyshev(n=5)
        self.assertEqual(t0, Poly(1))
        self.assertEqual(t1, Poly(1, 1))
        self.assertEqual(t2, Poly(-1) + Poly(2, 2))
        self.assertEqual(t3, Poly(-3, 1) + Poly(4, 3))
        self.assertEqual(t4, Poly(1) + Poly(-8, 2) + Poly(8, 4))
        self.assertEqual(t5, Poly(5, 1) + Poly(-20, 3) + Poly(16, 5))

    def test_legendre(self):
        p = self.poly_factory.legendre(n=self.N)
        #print p
        #print self.poly_factory.LEGENDRE   # sa wszystkie
        self.assertEqual(p.degree(), self.N)
        p0 = self.poly_factory.legendre(n=0)
        p1 = self.poly_factory.legendre(n=1)
        p2 = self.poly_factory.legendre(n=2)
        p3 = self.poly_factory.legendre(n=3)
        p4 = self.poly_factory.legendre(n=4)
        p5 = self.poly_factory.legendre(n=5)
        self.assertEqual(p0, Poly(1))
        self.assertEqual(p1, Poly(1, 1))
        self.assertEqual(p2, Poly(Fraction(-1, 2)) + Poly(Fraction(3, 2), 2))
        self.assertEqual(p3, Poly(Fraction(-3, 2), 1) + Poly(Fraction(5, 2), 3))
        self.assertEqual(p4, Poly(Fraction(3, 8)) 
            + Poly(Fraction(-15, 4), 2) + Poly(Fraction(35, 8), 4))
        self.assertEqual(p5, Poly(Fraction(15, 8), 1) 
            + Poly(Fraction(-35, 4), 3) + Poly(Fraction(63, 8), 5))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
