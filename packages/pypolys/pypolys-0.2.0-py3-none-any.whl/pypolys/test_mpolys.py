#!/usr/bin/env python3

import unittest
import random
from fractions import Fraction
from pypolys.mpolys import Poly


class TestPoly(unittest.TestCase):

    def setUp(self):
        self.x = Poly(1, 1)
        self.y = Poly(1, 0, 1)
        self.z = Poly(1, 0, 0, 1)

    def test_init(self):
        self.assertEqual(list(Poly()), [])
        self.assertEqual(list(Poly(2)), [(0,)]) # klucz domyslny
        self.assertEqual(list(Poly(2, 0)), [(0,)])
        self.assertEqual(list(Poly(2, 0, 0, 0)), [(0,)]) # klucz uciety
        self.assertEqual(list(Poly(0, 0, 0, 0)), [])
        self.assertEqual(list(Poly(0, 0, 1, 0)), [])
        self.assertEqual(list(Poly(2, 0, 1, 0)), [(0, 1)]) # klucz uciety

    def test_degree(self):
        self.assertEqual(Poly().degree(), 0)
        self.assertEqual(self.x.degree(), 1)
        self.assertEqual(self.y.degree(), 1)
        p = self.x * self.y
        self.assertEqual(p.degree(), 2)
        p = self.x * self.y * self.z
        self.assertEqual(p.degree(), 3)

    def test_len(self):
        self.assertEqual(len(Poly()), 0)
        self.assertEqual(len(self.x), 1)
        self.assertEqual(len(self.x + self.z), 2)

    def test_repr(self):
        self.assertEqual(repr(Poly()), "Poly()")
        self.assertEqual(repr(Poly(0)), "Poly()")
        self.assertEqual(repr(Poly(0, 0)), "Poly()")
        self.assertEqual(repr(Poly(0, 0, 0)), "Poly()")
        self.assertEqual(repr(Poly(0, 2)), "Poly()")
        self.assertEqual(repr(Poly(0, 2, 3)), "Poly()")
        self.assertEqual(repr(Poly(4)), "Poly(4, 0)")   # tu jest zero
        self.assertEqual(repr(self.x), "Poly(1, 1)")
        self.assertEqual(repr(self.y), "Poly(1, 0, 1)")
        self.assertEqual(repr(self.z), "Poly(1, 0, 0, 1)")
        self.assertEqual(repr(self.x + self.y), "Poly(1, 0, 1) + Poly(1, 1)")
        self.assertEqual(repr(Poly(Fraction(3, 1), 2, 1)), "Poly(3, 2, 1)")
        self.assertEqual(repr(Poly(Fraction(3, 5), 2, 1)), "Poly(Fraction(3, 5), 2, 1)")

    def test_fromiterable(self):
        self.assertEqual(Poly.fromiterable([0, 1]), self.x)
        self.assertEqual(Poly.fromiterable([0, 0, 1]), self.x * self.x)
        self.assertEqual(Poly.fromiterable([0, 1, 1]), self.x + self.x * self.x)

    def test_getitem(self):
        self.assertEqual(self.x[0], 0)   # int
        self.assertEqual(self.x[1], 1)   # int
        self.assertEqual(self.x[0,], 0)   # tuple
        self.assertEqual(self.x[1,], 1)   # tuple
        self.assertEqual(self.x[1, 0], 1)
        self.assertEqual(self.x[0, 1], 0)
        self.assertEqual(self.x[0, 0, 1], 0)
        self.assertEqual(self.y[0, 0], 0)
        self.assertEqual(self.y[0, 1], 1)
        self.assertEqual(self.z[0, 0, 1], 1)
        self.assertEqual(self.z[0, 1, 0], 0)

    def test_add_sub(self):
        self.assertEqual(self.x + self.x, Poly(2, 1))
        self.assertEqual(self.y + self.y, Poly(2, 0, 1))
        self.assertEqual(self.x - self.x, Poly())
        self.assertEqual(self.x + 3, self.x + Poly(3))
        self.assertEqual(3 + self.x, self.x + Poly(3))
        self.assertEqual(self.x - 3, self.x - Poly(3))
        self.assertEqual(3 - self.x, Poly(3) - self.x)

    def test_mul(self):
        self.assertEqual(self.x * self.x, Poly(1, 2))
        self.assertEqual(self.y * self.y, Poly(1, 0, 2))
        self.assertEqual(self.z * self.z, Poly(1, 0, 0, 2))
        self.assertEqual(self.x * self.y, Poly(1, 1, 1))
        self.assertEqual(self.x * self.z, Poly(1, 1, 0, 1))
        self.assertEqual(self.y * self.z, Poly(1, 0, 1, 1))
        self.assertEqual(self.x * self.y * self.z, Poly(1, 1, 1, 1))
        self.assertEqual(self.y * 3, Poly(3, 0, 1))
        self.assertEqual(3 * self.z, Poly(3, 0, 0, 1))

    def test_pos_neg(self):
        self.assertEqual(+self.x, self.x)
        self.assertEqual(-self.x, Poly(-1, 1))
        self.assertEqual(-self.y, Poly(-1, 0, 1))

    def test_pow(self):
        self.assertEqual(self.x ** 3, Poly(1, 3))
        self.assertEqual(self.y ** 5, Poly(1, 0, 5))
        p = self.x + Poly(1)
        self.assertEqual(p ** 3, p*p*p)
        self.assertEqual(p ** 5, p*p*p*p*p)
        p = self.y + Poly(2)
        self.assertEqual(p ** 3, p*p*p)

    def test_cancel(self):
        p = pow(self.x + self.y, 2) - Poly(2) * self.x * self.y
        self.assertEqual(len(p), 2)
        p = self.x ** 3 + Poly(-1, 3)
        self.assertEqual(len(p), 0)

    def test_div(self):
        self.assertEqual(repr(self.x / 2), "Poly(Fraction(1, 2), 1)")
        self.assertEqual(self.x / 2, Poly(Fraction(1, 2), 1))
        self.assertEqual(repr(self.x / 2.0), "Poly(0.5, 1)")
        self.assertEqual(repr(self.y / 2), "Poly(Fraction(1, 2), 0, 1)")
        self.assertEqual(repr(self.y / 2.0), "Poly(0.5, 0, 1)")
        self.assertEqual(Poly(6, 2, 3, 4) / Poly(2, 1, 2), Poly(3, 1, 1, 4))
        self.assertEqual(Poly(3, 2, 1) / Poly(2, 1, 1), Poly(Fraction(3, 2), 1))
        self.assertRaises(ValueError, lambda: self.x / self.y)
        self.assertRaises(ValueError, lambda: (self.x + self.z) / self.y)
        self.assertRaises(ValueError, lambda: self.x / (self.y + self.z))

    def test_lcm(self):
        self.assertEqual(self.x.lcm(1), self.x)
        self.assertEqual(self.x.lcm(self.y), self.x * self.y)
        self.assertEqual(self.z.lcm(self.y), self.z * self.y)
        self.assertRaises(ValueError, lambda: self.z.lcm(self.x + self.y))
        self.assertRaises(ValueError, lambda: (self.x + self.y).lcm(self.z))

    def test_diff(self):
        self.assertEqual(self.x.diff(2), Poly())
        self.assertEqual(self.z.diff(0), Poly())
        self.assertEqual(self.x.diff(0), Poly(1))
        self.assertEqual(self.y.diff(1), Poly(1))
        self.assertEqual(self.z.diff(2), Poly(1))
        p = Poly(3, 2, 5)
        self.assertEqual(p.diff(0), Poly(6, 1, 5))
        self.assertEqual(p.diff(1), Poly(15, 2, 4))
        self.assertEqual(p.diff(2), Poly())

    def test_integrate(self):
        self.assertEqual(self.x.integrate(0), Poly(Fraction(1, 2), 2))
        self.assertEqual(self.x.integrate(1), self.x * self.y)
        self.assertEqual(self.y.integrate(2), self.y * self.z)
        self.assertEqual(Poly(8, 3).integrate(0), Poly(2, 4))
        self.assertEqual(Poly(3, 2, 4).integrate(1), Poly(Fraction(3, 5), 2, 5))
        self.assertEqual(Poly(3, 0, 4).integrate(0), Poly(3, 1, 4))
        self.assertEqual(Poly(Fraction(3, 2), 1, 6, 4).integrate(2),
            Poly(Fraction(3, 10), 1, 6, 5))
        self.assertEqual(Poly(Fraction(3, 2), 1, 1).integrate(1),
            Poly(Fraction(3, 4), 1, 2))
        self.assertEqual(Poly(1.5, 1).integrate(0), Poly(0.75, 2))

    def test_combine(self):
        self.assertEqual(Poly(1, 3).combine(Poly(1, 2), var=0), Poly(1, 6))
        self.assertEqual((self.x ** 3).combine(self.y ** 2, var=0), self.y ** 6)
        self.assertEqual(self.x.combine(self.y ** 2, var=0), self.y ** 2)
        self.assertEqual(self.x.combine(self.y, var=2), self.x)
        self.assertEqual((self.x ** 2).combine(self.z + 3 * self.y, var=0), 
            self.z ** 2 + 6 * self.z * self.y + 9 * self.y ** 2)
        self.assertEqual((self.x ** 2 + self.y).combine(self.x ** 2, var=1),
            2 * self.x ** 2)
        # combine() wlasciwie realizuje eval().
        self.assertEqual(Poly(1, 3).combine(2, var=0), 8)
        self.assertEqual(Poly(1, 0, 3).combine(2, var=1), 8)
        self.assertEqual((Poly(3, 1, 2) + Poly(5, 0, 2, 1)).combine(
            2 * self.x, var=1), Poly(12, 3) + Poly(20, 2, 0, 1))

    def test_sort(self):
        lex_list = [Poly(1), self.z, self.z ** 2, 
            self.y, self.y * self.z, self.y **2, 
            self.x, self.x * self.z, self.x * self.y, self.x ** 2]
        deglex_list = [Poly(1), self.z, self.y, self.x,
            self.z ** 2, self.y * self.z, self.y ** 2,
            self.x * self.z, self.x * self.y, self.x ** 2]
        blist = list(deglex_list)
        random.shuffle(blist)
        # Sortowanie wielomianow.
        blist.sort(key=Poly.degree)
        self.assertEqual(blist[0].degree(), 0)
        self.assertEqual(blist[1].degree(), 1)
        self.assertEqual(blist[2].degree(), 1)
        self.assertEqual(blist[3].degree(), 1)
        self.assertEqual(blist[4].degree(), 2)
        blist.sort(key=Poly.key_lex)
        self.assertEqual(lex_list, blist)
        blist.sort(key=Poly.key_deglex)
        self.assertEqual(deglex_list, blist)

    def test_leading_term(self):
        p1 = pow(3 * self.x + 1, 2)
        self.assertEqual(p1.leading_term(key=Poly.key_lex), 9 * self.x ** 2)
        self.assertEqual(p1.leading_monomial(key=Poly.key_lex), self.x ** 2)
        self.assertEqual(p1.leading_coefficient(key=Poly.key_lex), 9)
        p1 = pow(3 * self.y + 1, 2)
        self.assertEqual(p1.leading_term(key=Poly.key_lex), 9 * self.y ** 2)
        self.assertEqual(p1.leading_monomial(key=Poly.key_lex), self.y ** 2)
        self.assertEqual(p1.leading_coefficient(key=Poly.key_lex), 9)
        p1 = pow(2 * self.x + self.y, 3)
        self.assertEqual(p1.leading_term(key=Poly.key_lex), 8 * self.x ** 3)
        self.assertEqual(p1.leading_monomial(key=Poly.key_lex), self.x ** 3)
        self.assertEqual(p1.leading_coefficient(key=Poly.key_lex), 8)
        self.assertEqual(Poly(5).leading_term(key=Poly.key_lex), Poly(5))
        self.assertEqual(Poly(5).leading_monomial(key=Poly.key_lex), Poly(1))
        self.assertEqual(Poly(5).leading_coefficient(key=Poly.key_lex), 5)
        self.assertRaises(ValueError, Poly().leading_term, Poly.key_lex)
        self.assertRaises(ValueError, Poly().leading_monomial, Poly.key_lex)
        self.assertRaises(ValueError, Poly().leading_coefficient, Poly.key_lex)

    def test_iterterms(self):
        p1 = pow(self.x * self.y + 1, 2)
        #print list(p1.iterterms())
        self.assertEqual(len(list(p1.iterterms())), 3)
        self.assertEqual(set(term.degree() for term in p1.iterterms()), set([0, 2, 4]))
        self.assertEqual(sum(term.degree() for term in p1.iterterms()), 6)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
