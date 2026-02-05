# -----------------------------------------------------------------------------
# Exercise 1 - The requirements
#
# "I used the code in frac.py and I lost all sorts of points. For
# example, I produced one answer of (6, 12). The teacher wanted (1, 2)
# instead. Can you change the code to put answers in lowest terms?"
#
# "Also, the teacher told us to never put a negative number in the
# denominator.  So, you'd never write (2, -3).  Instead you'd write
# (-2, 3).  Also, (-2, -3) should just be written as (2, 3)."
#
# "And last, but not least, what is with that code you wrote?  I can
# hardly read anything that's going on in there with all of that tuple
# indexing."
#
# To fix all of these problems, you decide to introduce a few helper
# functions.  A make_frac() function will be used to construct the
# tuples and put things in lowest terms. To hide tuple indexing,
# you'll use numerator() and denominator() functions.


"""
Reasoning:
We have this fraction but its written as tuples
Proposition is that maybe the fraction code should be written to some
kind of interface layer; below the interface layer we can use tuples to

    ------------------
    |    fractions    |
    ------------------
      |            |
      |            |
      V            |
    --------       |
    |tuples|       |
    --------       |
                   |
                   V
                 ----------
                 |interface|
                 -----------
                    |             
                    |             
                    V             
                --------   can change      -----
                |tuples|  ------------>    |dict|
                --------                    -----

                
More verbose but more descriptive 
Abstraction to make it more friendly               

you can change the underlying representation without changing
the interface layer; from tuples to dicts
"""



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


def add_frac_0(a, b):
    res = (a[0] * b[1] + a[1] * b[0], a[1] * b[1])
    return lowest_term(res[0], res[1])


def sub_frac_0(a, b):
    res = (a[0] * b[1] - a[1] * b[0], a[1] * b[1])
    return lowest_term(res[0], res[1])


def mul_frac_0(a, b):
    res = (a[0] * b[0], a[1] * b[1])
    return lowest_term(res[0], res[1])


def div_frac_0(a, b):
    res = (a[0] * b[1], a[1] * b[0])
    return lowest_term(res[0], res[1])


a = (2, 3)
b = (3, 4)
assert mul_frac_0(a, b) == (1, 2)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@ Solution @@@@@@@@@@@@@@@@@@@@@@@@@@@@


def make_frac(n, d):
    return lowest_term(n, d)


def numerator(n):
    return n[0]

def denominator(n):
    return n[1]


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