# -----------------------------------------------------------------------------
# Exercise 3
#
# During your coffee break, you decide to show your fraction code to a
# Lisp programmer at the office.
#
# "You know, you could really shatter 5th grade minds if you
# represented fractions entirely as a function.  Here, something like
# this:"

def gcd(a, b):
    # Greatest common divisor
    while b:
        a, b = b, a % b
    return a

def make_frac(numer, denom):
    d = gcd(numer, denom)
    numer = numer // d
    denom = denom // d

    """
    Instead of storing a fraction as a data structure (like a tuple or class), 
    this code represents a fraction as a function that "knows" its numerator 
    and denominator through closure.

    This is an example of data abstraction — the fraction's representation (a function) 
    is hidden behind an interface (numerator/denominator), so you could change the 
    implementation later without breaking code that uses it.
    
    as long as you observe the interface: you can do funky stuff
    
    inner function keeps all vars in the outter function's scope alive
    closure: function + referencing environment    
    """

    def frac(s):
        # frac(s) "captures" the numer and denom values
        return numer if s else denom
    return frac

def numerator(f):
    # for (2, 3) -> # calls a(True)  → returns 2
    return f(True)

def denominator(f):
    # for (2, 3) -> # calls a(False) → returns 3
    return f(False)


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


# Unit tests.  This is the same set of tests as before.  NO CHANGES MADE.
def test_frac():
    a = make_frac(4, 6) # # a is now a FUNCTION, not data
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

# As you collect the pieces of your brain, ponder the fact that those
# top level functions make_frac(), numerator(), and denominator()
# really saved you a lot of hassle here.   Yes, the underlying
# representation changed into something else, but none of the
# higher level code had to change.
