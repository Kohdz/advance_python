# -----------------------------------------------------------------------------
# Exercise 6
#
# Modeling fractions as a data structure with a collection of
# standalone functions isn't very "Pythonic."  Python has a protocol
# for manipulating numbers via operators such as +, -, *, and /.
# These operators are mapped to methods such as __add__() and __mul__().
#
# In this exercise, we're going to write a Fraction class that works
# like a proper Python number. To do this, you'll need to implement a
# variety of so-called "magic" methods such as __add__, __sub__,
# __mul__, etc.  Some later stages of the exercise have you make it a
# bit nicer to work with by implementing a few other methods.
#
# However, as a twist of fate, you are going to be required to
# continue supporting the "old" programming interface.  As often is
# the case in a project, you've to support both old and new code at
# the same time.  So, we've got to think about that.
#
# There are various test functions in this file that need to pass.
# Read ahead and comment them out as you work.
#
# Note: The README.md file has additional details about redefining
# Python magic methods.
# -----------------------------------------------------------------------------

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# We will define a proper class
class Fraction:
    def __init__(self, numerator, denominator):
        d = gcd(numerator, denominator)
        self.numerator = numerator // d
        self.denominator = denominator // d

    # Define various magic methods for Python operators
    def __add__(self, other):
        return add_frac(self, other)

    def __sub__(self, other):
        return sub_frac(self, other)
    
    def __mul__(self, other):
        return mul_frac(self, other)

    
    def __truediv__(self, other):
        return div_frac(self, other)
    
    # __radd__ == __add__
    
    def __radd__(self, other):
        return add_frac(other, self)

    def __rsub__(self, other):
        return sub_frac(other, self)
        
    def __rmul__(self, other):
        return mul_frac(other, self)

    def __eq__(self, other):
        return self.numerator/self.denominator == other.numerator/self.denominator

    def __ne__(self, other):
        # a != b 
        return self.numerator/self.denominator != other.numerator/self.denominator

    def __le__(self, other):
        # a <= b 
        return self.numerator/self.denominator <= other.numerator/self.denominator

    def __lt__(self, other):
        # a < b 
        return self.numerator/self.denominator < other.numerator/self.denominator

    def __ge__(self, other):
        # a >= b  
        return self.numerator/self.denominator >= other.numerator/self.denominator

    def __gt__(self, other):
        # a > b  
        return self.numerator/self.denominator > other.numerator/self.denominator

        # b = Fraction(2, 1)
        # assert str(b) == '2'

        # c = Fraction(0, 2)
        # assert str(c) == '0'

    def __str__(self):
        if self.numerator == 0:
            return '0'
        elif self.denominator == 1:
            return str(self.numerator)
        else:
            return f"{self.numerator}/{self.denominator}"

    def __float__(self):
        return self.numerator/self.denominator
    
    def __int__(self):
        return self.numerator//self.denominator

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

    def __hash__(self):
        return hash((self.numerator, self.denominator))



# Legacy interface.   We'll continue to support it for backwards compatibility
def make_frac(numerator, denominator):
    return Fraction(numerator, denominator)

def numerator(f):
    return f.numerator

def denominator(f):
    return f.denominator

# Design discussion.   This is the old interface of the fraction operations.
# Should the new interface be implemented using these functions?  For example:
#
#     class Fraction:
#         ...
#         def __add__(self, other):
#             return add_frac(self, other)
#
# Or should the old interface be supported in terms of the new interface?
# For example:
#
#      def add_frac(a, b):
#          return a + b

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


# The old unit tests must still pass (legacy code)
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

# New unit tests.  These manipulate fractions as proper Python numbers.
def test_math():
    a = Fraction(4, 6)
    assert (a.numerator, a.denominator) == (2, 3)

    b = Fraction(-3, -4)
    assert (b.numerator, b.denominator) == (3, 4)

    # Requires the __add__() method
    c = a + b
    assert (c.numerator, c.denominator) == (17, 12)

    # Requires the __sub__() method
    d = a - b
    assert (d.numerator, d.denominator) == (-1, 12)

    # Requires the __mul__() method
    e = a * b
    assert (e.numerator, e.denominator) == (1, 2)

    # Returns the __truediv__() method
    f = a / b
    assert (f.numerator, f.denominator) == (8, 9)

    # Mixed type operations.  Note: Python integers
    # already have .numerator and .denominator attributes

    g = a + 1
    assert (g.numerator, g.denominator) == (5, 3)

    # Requires the __radd__() method
    g = 1 + a
    assert (g.numerator, g.denominator) == (5, 3)

    # Requires the __rsub__() method
    g = 1 - a
    assert (g.numerator, g.denominator) == (1, 3)
    
    h = a * 10
    assert (h.numerator, h.denominator) == (20, 3)

    # Requires the __rmul__() method
    h = 10 * a
    assert (h.numerator, h.denominator) == (20, 3)

    # Comparisons.  For these, you'll need to implement
    # methods such as __eq__(), __ne__(), __lt__(), __le__(),
    # __gt__(), and __ge__().
    #
    # To compare fractions you can perform comparisons like this:
    #
    # a = Fraction(2, 3)
    # b = Fraction(4, 5)
    #
    # a < b  ==> a.numerator * b.denominator < a.denominator * b.numerator

    assert a < b
    assert a <= b
    assert a != b
    assert b > a
    assert b >= a
    assert a == Fraction(2, 3)

    print('Good math')

test_math()

# -----------------------------------------------------------------------------
# Niceties
#
# There are certain things you can do to make your objects play nicer
# with the rest of Python.  These include nice printing, debugging,
# and numeric conversions.
#
# Modify your Fraction class so that it additionally passes the following tests
# -----------------------------------------------------------------------------

def test_nice():
    a = Fraction(3, 2)

    assert str(a) == '3/2'                # Requires the __str__() method
    assert repr(a) == 'Fraction(3, 2)'    # Requires the __repr__() method
    assert float(a) == 1.5                # Requires the __float__() method
    assert int(a) == 1                    # Requires the __int__() method

    # Special cases of nice output
    b = Fraction(2, 1)
    assert str(b) == '2'

    c = Fraction(0, 2)
    assert str(c) == '0'

    print('Nice fractions')

# Uncomment when ready
test_nice()

