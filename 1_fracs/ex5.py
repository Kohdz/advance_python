# -----------------------------------------------------------------------------
# Exercise 5
#
# The function make_frac() is used to construct fractions. One feature
# of make_frac() is that it puts a fraction number into lowest terms and
# normalizes the sign to always appear in the numerator.  For example:
#
#    >>> a = make_frac(4, -6)
#    >>> a.numerator
#    -2
#    >>> a.denominator
#    3
#    >>>
#
# How would you modify the Fraction namedtuple class to have the same
# behavior if you used its normal constructor?
#
#    >>> a = Fraction(4, -6)
#    >>> a.numerator
#    -2
#    >>> a.denominator
#    3
#    >>>
#
# Disclaimer:  This is hard and not obvious.  But, it points to deeper
# problems. Maybe NamedTuple is not the solution we seek.
# -----------------------------------------------------------------------------


"""
In python your normally thinking of objects
Your not thinking about make_frac(), etc


Not Pythonic
a = make_frac(4, 6)
a == Fraction(numerator=4, denominator=6)


Is Pythonic
b = Fraction(2, 3)
isisntance(b, Fraction) == True
b.numerator == 2
b.denominator == 3
"""




from typing import NamedTuple

def gcd(a, b):
    # Greatest common divisor
    while b:
        a, b = b, a % b
    return a

class Fraction(NamedTuple):
    numerator : int
    denominator : int
    # You'll need to make modifications to pass the test below.  Logically,
    # you'll want to make it so the numerator/denominator are reduced to
    # lowest terms as you might have done in an __init__() method.  Sadly,
    # doing that does NOT work (can you figure out why?)

    # DOES NOT WORK!  Can you think of an alternative that achieves the same
    # effect?
    # self is an already created object
    # so its a tuple, when we do `self.numerator = ...` we are trying to
    # change the tuple, which is immutable
    def __init__(self, numerator, denominator):
        d = gcd(numerator, denominator)
        self.numerator = numerator // d
        self.denominator = denominator // d

    """
    When you do p = Point(2, 3)
    there are actually two steps
    
    p = Point.__new__(Point, 2, 3) # unintialized object
    that creates the object
    the object has no data in it
    p.__dict == {}

    then python calls `__init__` on it
    p.__init__(2, 3)

    """
    # new gets called after object creation
    # does not work
    def __new__(cls, numerator, denominator):
        d = gcd(numerator, denominator)
        numerator = numerator // d
        denominator = denominator // d
        return super().__new__(cls, numerator, denominator) # Orginal new
    
    """
    hit classes in python are storedd as a data class

    class Point:
        x: int
        y: int

    Point.__annotations__ == {'x': <class int>, 'y': <class int>}
    Python creates a string and populates it with the field names
    the string gets run through exec to create the class
    the result of exec is attached to the class

    - type hints create -> string "def __new__(...) which is run through exec
    which is attached to the class
    
    in other words you cant define the new, because exec wants to define it for you
    """

    """
    you can stick methods to the clas 

    class Example:
        def __init__(self, x):
            self.x = x

    e = Example(3)
    e.x == 3

    def yow(self):
        print("Yow!", self.x)

    Example.yow = yow
    e.yow()  # prints "Yow! 3"    
    """

    """
    data classes is doing exactually the same thing as type hints
    """

    """
    NamedTuple is crazy town

    NamedTuple is a function!!!
    but a class cannot inherit from a function

    """


# Solution: works because the code generation catches self, but does not
# catch child class

class _Fraction_1(NamedTuple):
    numerator : int
    denominator : int
    # You'll need to make modifications to pass the test below.  Logically,
    # you'll want to make it so the numerator/denominator are reduced to
    # lowest terms as you might have done in an __init__() method.  Sadly,
    # doing that does NOT work (can you figure out why?)

    # DOES NOT WORK!  Can you think of an alternative that achieves the same
    # effect?
    # self is an already created object
    # so its a tuple, when we do `self.numerator = ...` we are trying to
    # change the tuple, which is immutable
    def __init__(self, numerator, denominator):
        d = gcd(numerator, denominator)
        self.numerator = numerator // d
        self.denominator = denominator // d

class Fraction_1(_Fraction_1):
    def __new__(cls, numerator, denominator):
        d = gcd(numerator, denominator)
        numerator = numerator // d
        denominator = denominator // d
        return super().__new__(cls, numerator, denominator) # Orginal new


# You are not allowed to change any part of this test.
def test_frac():
    a = Fraction(4, 6)
    assert a.numerator == 2
    assert a.denominator == 3
    assert isinstance(a, Fraction)

    b = Fraction(-3, -4)
    assert b.numerator == 3
    assert b.denominator == 4

    c = Fraction(3, -4)
    assert c.numerator == -3
    assert c.denominator == 4

    print("Good fractions")

test_frac()

# ----------------------------------------------------------------------
# Even if you could get this work, there are other issues.
#
# Just as integers "accidentally" work as Fractions. A Fraction
# defined as a NamedTuple accidentally works as a tuple.  That means
# that it supports various "tuple" operations like this:
#
#     >>> a = Fraction(2, 3)
#     >>> len(a)
#     2
#     >>> a[0]
#     2
#     >>> a + Fraction(4, 5)
#     (2, 3, 4, 5)
#     >>>
#
# Is this a good thing or not?




