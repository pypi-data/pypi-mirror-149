#!/usr/bin/env python3

import unittest
import random
from fractions import Fraction
from pypolys.polys import Poly


class TestPoly(unittest.TestCase):

    def setUp(self):
        self.x0 = Poly(1)
        self.x1 = Poly(1, 1)
        self.x2 = Poly(1, 2)
        self.x3 = Poly(1, 3)

    def test_repr(self):
        self.assertEqual(repr(Poly()), "Poly()")
        self.assertEqual(repr(Poly(0)), "Poly()")
        self.assertEqual(repr(Poly(0, 2)), "Poly()")
        self.assertEqual(repr(Poly(2, 0)), "Poly(2)")
        self.assertEqual(repr(self.x1 + self.x2), "Poly(1, 1) + Poly(1, 2)")
        self.assertEqual(repr(Poly(Fraction(3, 1), 2)), "Poly(3, 2)")
        self.assertEqual(repr(Poly(Fraction(3, 5), 2)), "Poly(Fraction(3, 5), 2)")

    def test_fromiterable(self):
        self.assertEqual(Poly.fromiterable([0, 1]), self.x1)
        self.assertEqual(Poly.fromiterable([0, 0, 1]), self.x2)
        self.assertEqual(Poly.fromiterable([0, 1, 1]), self.x1 + self.x2)

    def test_is_zero(self):
        self.assertTrue(Poly().is_zero())
        self.assertTrue(Poly(0, 2).is_zero())
        self.assertFalse(self.x1.is_zero())

    def test_degree(self):
        self.assertEqual(self.x0.degree(), 0)
        self.assertEqual(self.x1.degree(), 1)
        self.assertEqual(self.x2.degree(), 2)
        self.assertEqual(self.x3.degree(), 3)

    def test_len(self):
        self.assertEqual(len(Poly()), 0)
        self.assertEqual(len(self.x1), 1)
        self.assertEqual(len(self.x1 + self.x3), 2)

    def test_getitem(self):
        self.assertEqual(self.x2[0], 0)
        self.assertEqual(self.x2[1], 0)
        self.assertEqual(self.x2[2], 1)
        self.assertEqual(self.x2[3], 0)

    def test_add_sub(self):
        self.assertEqual(self.x2 + self.x2, Poly(2, 2))
        self.assertEqual(self.x1 - self.x1, Poly())
        self.assertEqual(self.x2 + 3, self.x2 + Poly(3))
        self.assertEqual(3 + self.x2, self.x2 + Poly(3))
        self.assertEqual(self.x2 - 3, self.x2 - Poly(3))
        self.assertEqual(3 - self.x2, Poly(3) - self.x2)

    def test_mul(self):
        self.assertEqual(self.x1 * self.x1, self.x2)
        self.assertEqual(self.x1 * self.x2, self.x3)
        self.assertEqual(self.x2 * 3, Poly(3, 2))
        self.assertEqual(3 * self.x2, Poly(3, 2))

    def test_pos_neg(self):
        self.assertEqual(+self.x1, self.x1)
        self.assertEqual(-self.x1, Poly(-1, 1))
        self.assertEqual(-self.x2, Poly(-1, 2))

    def test_combine(self):
        self.assertEqual(self.x3.combine(self.x2), Poly(1, 6))
        self.assertEqual(self.x2.combine(self.x3), Poly(1, 6))
        self.assertEqual(self.x2.combine(self.x1 + Poly(3)), 
            self.x2 + Poly(6, 1) + Poly(9))

    def test_pow(self):
        self.assertEqual(self.x1 ** 3, self.x3)
        p = self.x1 + Poly(1)
        self.assertEqual(p ** 3, p*p*p)
        self.assertEqual(p ** 5, p*p*p*p*p)
        self.assertEqual(pow(self.x1, 5).combine(p), p*p*p*p*p)
        self.assertEqual(Poly(1, 5).combine(p), p*p*p*p*p)

    def test_eval(self):
        self.assertEqual(self.x2.eval(2), 4)
        self.assertEqual(self.x3.eval(3), 27)

    def test_diff(self):
        self.assertEqual(self.x0.diff(), Poly())
        self.assertEqual(self.x1.diff(), self.x0)
        self.assertEqual(self.x3.diff(), Poly(3, 2))

    def test_integrate(self):
        self.assertEqual(Poly(2, 1).integrate(), self.x2)
        self.assertEqual(self.x1.integrate(), Poly(Fraction(1, 2), 2))
        self.assertEqual(self.x2.integrate(), Poly(Fraction(1, 3), 3))
        self.assertEqual(Poly(3, 4).integrate(), Poly(Fraction(3, 5), 5))
        self.assertEqual(Poly(Fraction(3, 2), 1).integrate(), Poly(Fraction(3, 4), 2))
        self.assertEqual(Poly(Fraction(3, 2), 1).integrate(), Poly(0.75, 2))
        self.assertEqual(Poly(1.5, 1).integrate(), Poly(0.75, 2))

    def test_call(self):
        self.assertEqual(self.x2(self.x3), Poly(1, 6))
        self.assertEqual(self.x2(2), 4)

    def test_div(self):
        self.assertEqual(self.x2 / 2.0, Poly(0.5, 2))
        self.assertEqual(self.x2 / 2, Poly(Fraction(1, 2), 2))
        self.assertEqual(self.x2 / Fraction(1, 2), Poly(2, 2))
        self.assertEqual(repr(self.x3 / 2), "Poly(Fraction(1, 2), 3)")
        self.assertEqual(repr(self.x3 / 2.0), "Poly(0.5, 3)")
        self.assertEqual(self.x3 / self.x2, self.x1)
        self.assertEqual(self.x3 / self.x3, self.x0)
        self.assertEqual(Poly(6, 5) / Poly(3, 2), Poly(2, 3))
        self.assertRaises(ValueError, lambda: self.x1 / self.x2)
        self.assertRaises(ValueError, lambda: self.x3 / (self.x2 + self.x1))
        self.assertRaises(ValueError, lambda: (self.x3 + self.x2) / self.x1)

    def test_lcm(self):
        self.assertEqual(self.x2.lcm(1), self.x2)
        self.assertEqual(self.x2.lcm(self.x3), self.x3)
        self.assertRaises(ValueError, lambda: self.x1.lcm(self.x2 + self.x3))
        self.assertRaises(ValueError, lambda: (self.x1 + self.x2).lcm(self.x3))

    def test_cancel(self):
        p1 = pow(self.x1 + 1, 2) - self.x2
        self.assertEqual(p1.degree(), 1)
        p1 = self.x3 + Poly(-1, 3)
        self.assertEqual(p1.degree(), 0)

    def test_sort(self):
        alist = [self.x0, self.x1, self.x2, self.x3]
        blist = list(alist)
        # Sortowanie wg stopni wielomianow.
        random.shuffle(blist)
        blist.sort(key=Poly.degree)
        self.assertEqual(alist, blist)
        random.shuffle(blist)
        blist.sort(key=Poly.key_lex)
        self.assertEqual(alist, blist)
        random.shuffle(blist)
        blist.sort(key=Poly.key_deglex)
        self.assertEqual(alist, blist)

    def test_leading_term(self):
        p1 = pow(3 * self.x1 + 1, 2)
        self.assertEqual(p1.leading_term(key=Poly.key_lex), 9 * self.x2)
        self.assertEqual(p1.leading_monomial(key=Poly.key_lex), self.x2)
        self.assertEqual(p1.leading_coefficient(key=Poly.key_lex), 9)
        p1 = pow(5 * self.x1 + 2, 3)
        self.assertEqual(p1.leading_term(key=Poly.key_lex), 125 * self.x3)
        self.assertEqual(p1.leading_monomial(key=Poly.key_lex), self.x3)
        self.assertEqual(p1.leading_coefficient(key=Poly.key_lex), 125)
        self.assertRaises(ValueError, Poly().leading_term, Poly.key_lex)
        self.assertRaises(ValueError, Poly().leading_monomial, Poly.key_lex)
        self.assertRaises(ValueError, Poly().leading_coefficient, Poly.key_lex)
        self.assertEqual(Poly(5).leading_term(key=Poly.key_lex), Poly(5))
        self.assertEqual(Poly(5).leading_monomial(key=Poly.key_lex), Poly(1))
        self.assertEqual(Poly(5).leading_coefficient(key=Poly.key_lex), 5)

    def test_iterterms(self):
        p1 = pow(self.x2 + 1, 2)
        self.assertEqual(len(list(p1.iterterms())), 3)
        self.assertEqual(set(term.degree() for term in p1.iterterms()), set([0, 2, 4]))
        self.assertEqual(sum(term.degree() for term in p1.iterterms()), 6)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
