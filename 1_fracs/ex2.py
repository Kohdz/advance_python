# -----------------------------------------------------------------------------
# Exercise 2
#
# "Dad? Tuples? Accessor functions? Really? What is this?"
#
# Grumbling, Peter starts thinking about the general design problem of
# data abstraction.  Despite his use of tuples, the functionality of
# his code is still fairly well organized into layers.  For example,
# none of the core math functions (add_frac, sub_frac, mul_frac, etc.)
# know anything about tuples.  Instead, they use the accessor
# functions such as numerator(r) and denominator(r).  Fractions are
# always constructed using make_frac().  Abstraction is good.
#
# "I'll show her!"
#
# Peter decides that he can easily change his code to use dictionaries
# without breaking anything else.  All he needs to do is change the
# make_frac(), numerator(), and denominator() functions.  Nothing else
# needs to change, including the tests.


def gcd(a, b):
    # Take absolute values so GCD works for negative numbers
    a, b = abs(a), abs(b)

    # Euclidean algorithm:
    # Repeatedly replace (a, b) with (b, a % b)
    # until b becomes 0
    while b != 0:
        a, b = b, a % b

    # When b == 0, a is the GCD
    return a


def lowest_term(n, d):
    g = gcd(n, d)
    # Divide by the GCD
    n //= g
    d //= g

    # Normalize the sign:
    # Keep the denominator positive
    if d < 0:
        n = -n
        d = -d

    return (n, d)


def make_frac(n, d):
    n, d = lowest_term(n, d)
    # idea is that if you program through an interface,
    # you can change the internals as you like
    return {
        "numerator": n,
        "denominator": d,
    }


def numerator(n):
    return n.get("numerator")


def denominator(n):
    return n.get("denominator")


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


def test_frac():
    a = make_frac(2, 3)
    assert (numerator(a), denominator(a)) == (2, 3)

    b = make_frac(3, 4)
    assert (numerator(b), denominator(b)) == (3, 4)

    c = make_frac(3, -4)
    assert (numerator(c), denominator(c)) == (-3, 4)

    d = add_frac(a, b)
    assert (numerator(d), denominator(d)) == (17, 12)


test_frac()
