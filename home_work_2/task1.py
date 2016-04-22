#! usr/bin/env python
import sys


class Rational(object):

    def __init__(self, numerator=0, denominator=1):
        gcd = self._gcd(abs(numerator), abs(denominator))
        if (denominator < 0):
            denominator = -denominator
            numerator = -numerator
        self.numerator = numerator / gcd
        self.denominator = denominator / gcd

    def _gcd(self, a, b):
        if (b > a):
            tmp = a
            a = b
            b = tmp
        while(b > 0):
            r = a % b
            a = b
            b = r
        return a

    def __add__(self, other):
        new_denom = self.denominator * other.denominator
        new_num = (self.numerator * other.denominator +
                   self.denominator * other.numerator)
        return Rational(new_num, new_denom)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __mul__(self, other):
        new_num = self.numerator * other.numerator
        new_denom = self.denominator * other.denominator
        return Rational(new_num, new_denom)

    def __div__(self, other):
        new_num = self.numerator * other.denominator
        new_denom = self.denominator * other.numerator
        return Rational(new_num, new_denom)

    def __eq__(self, other):
        return (self.numerator * other.denominator ==
                self.denominator * other.numerator)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

exec(sys.stdin.read())
