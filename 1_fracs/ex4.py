# -----------------------------------------------------------------------------
# Exercise 4
#
# "Dad, have you ever considered using a named tuple?"
#
# Background:  Named tuples are a feature of Python that has been around
# since version 2.6, released over a decade ago. They're commonly seen in
# programming recipes as a quick "hack" for making a class-like data structure.
# Older versions of Python used a code-generation function in the collections
# module:
#
#     Fraction = collections.namedtuple('Fraction', ['numerator', 'denominator'])
#
# The version below is a more modern variant provided by the typing module.

"""
NamedTuples Really solves an issue about interfaces

Say you have your application
works on an interface; so you an change things at a low level

    ------------------
    |    app    |
    ------------------
      |            |
      |            |
      V            |
    --------       |
    |tuples|       |
    --------       |
                   |
                   V
                ----------   cant change (easy)   -------------
                |interface|  --------------->    |new interface|
                -----------                      -------------
                    |
                    |
                    V
                --------   can change      -----
                |tuples|  ------------>    |dict|
                --------                    -----


What if you wanted to change the interface? that brakes the universe
A expense process to break interface

NamedTuples solves with interface change problem

import time
t = time.localtime()
len(t) == 9

ininstance(t, tuple)
True

t[0] == 2025
t[1] == 3
people did not like having to do t[0] to get the year


NamedTuple is a way of evolving tuples to be more class liked
Named Tuples gives you attribute access with dot notation
and DOES NOT BREAK BACKWARDS COMPATIBILITY

t.tm_year == 2025
t.tm_mon == 3
"""

from typing import NamedTuple


class Fraction(NamedTuple):
    numerator: int
    denominator: int


def gcd(a, b):
    # Greatest common divisor
    while b:
        a, b = b, a % b
    return a


def make_frac(numer, denom):
    d = gcd(numer, denom)
    return Fraction(numer // d, denom // d)


def numerator(f):
    return f.numerator


def denominator(f):
    return f.denominator


def add_frac(a, b):
    return make_frac(
        numerator(a) * denominator(b) + denominator(a) * numerator(b),
        denominator(a) * denominator(b),
    )


def sub_frac(a, b):
    return make_frac(
        numerator(a) * denominator(b) - denominator(a) * numerator(b),
        denominator(a) * denominator(b),
    )


def mul_frac(a, b):
    return make_frac(numerator(a) * numerator(b), denominator(a) * denominator(b))


def div_frac(a, b):
    return make_frac(numerator(a) * denominator(b), denominator(a) * numerator(b))


# Unit tests. These are the same tests as before. NO CHANGES MADE.
def test_frac():
    a = make_frac(4, 6)
    assert (numerator(a), denominator(a)) == (2, 3)

    b = make_frac(-3, -4)
    assert (numerator(b), denominator(b)) == (3, 4)

    c = make_frac(3, -4)
    assert (numerator(c), denominator(c)) == (-3, 4)

    d = add_frac(a, b)
    assert (numerator(d), denominator(d)) == (17, 12)

    e = sub_frac(a, b)
    assert (numerator(e), denominator(e)) == (-1, 12)

    f = mul_frac(a, b)
    assert (numerator(f), denominator(f)) == (1, 2)

    g = div_frac(a, b)
    assert (numerator(g), denominator(g)) == (8, 9)

    print("Good fractions")


test_frac()

# ----------------------------------------------------------------------
# Did you know that the math functions can now also work with normal
# integers if you implement the accessor functions so that they use
# the dot (.) for attribute access?  Try this:
#
#     def numerator(a):
#         return a.numerator
#
#     def denominator(a):
#         return a.denominator
#
# Verify that it works:
#
#     >>> a = make_frac(2, 3)
#     >>> b = add_frac(a, 1)
#     >>> b
#     Fraction(numerator=5, denominator=3)
#     >>>
#
# You can even just use integers
#
#     >>> c = add_frac(2, 3)
#     >>> c
#     Fraction(numerator=5, denominator=1)
#     >>>
#
# Can you explain why this works?
