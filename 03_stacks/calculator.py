# calculator.py
#
# Don't work on this part until you have first finished stacks.py.
#
# Abstraction or Distraction?
# ---------------------------
# What is the actual problem being solved here?  Is the end goal to
# create a Stack or are we trying to create a Calculator?
# Go read the first part of stacks.py again.... wait, it's actually
# all about calculators!
#
# Discussion: Is time spent worrying about Stacks as a separate object
# worth the extra effort?  Maybe not.

# -----------------------------------------------------------------------------
# Exercise 7 - Only a Calculator
#
# Define a Calculator class that has the same functionality as before,
# but which doesn't bother with all of the extra stack class code.
# While we're at it, we might as well give the calculator a few
# extra functions like square roots, powers, swapping stack items
# and so forth.  Your class should pass the tests below.
#
# Discussion: One of the core tenets of object-oriented programming is
# the idea of "encapsulation."  There is some high-level functionality that a
# Calculator is supposed to provide.  What happens inside isn't
# supposed to matter--this includes details about how the internals
# are actually put together.
#
# No stack = one less thing to worry about!

import math


class NotEnoughValues(Exception):
    pass

class Calculator:
    def __init__(self):
        self._values = []                      # Should *NOT* depend on a separate Stack class
        
    def push(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Can only push numbers")
        self._values.append(value)

    def pop(self):
        return self._values.pop()

    def _pop2(self):
        if len(self._values) < 2:
            raise NotEnoughValues("not enough values")
        return (self.pop(), self.pop())

    def swap(self):           # Swap top two stack items
        right, left = self._pop2()
        self.push(right)
        self.push(left)

    def add(self):
        right, left = self._pop2()
        self.push(left + right)

    def sub(self):
        right, left = self._pop2()
        self.push(left - right)

    def mul(self):
        right, left = self._pop2()
        self.push(left*right)

    def div(self):
        right, left = self._pop2()
        self.push(left//right)

    def pow(self):            # Power
        exp, base = self._pop2()
        self.push(base ** exp)

    def sqrt(self):           # Computes sqrt of the top. Use math.sqrt
        if len(self._values) < 1:
            raise NotEnoughValues("not enough values")
        self.push(math.sqrt(self.pop()))
        

def test_calculator(calc):
    calc.push(23)
    calc.push(45)
    calc.add()
    assert calc.pop() == 68

    calc.push(2)
    calc.push(3)
    calc.push(4)
    calc.add()
    calc.mul()
    assert calc.pop() == 14

    calc.push(10)
    calc.push(3)
    calc.sub()
    assert calc.pop() == 7

    calc.push(10)
    calc.push(5)
    calc.div()
    assert calc.pop() == 2.0

    calc.push(10)
    calc.push(2)
    calc.pow()
    assert calc.pop() == 100

    calc.push(100)
    calc.sqrt()
    assert calc.pop() == 10.0

    calc.push(2)
    calc.push(3)
    calc.swap()
    assert calc.pop() == 2
    assert calc.pop() == 3
    
    # Make sure that only numeric values can be pushed
    calc.push(2)
    calc.push(2.5)
    try:
        calc.push("two")
    except TypeError as err:
        pass
    else:
        assert False, "Bad Calculator!"
    
    print("Good calculator!")

test_calculator(Calculator())

# -----------------------------------------------------------------------------
# Exercise 8 - The Script
#
# Mel wants to know if common calculations can be "scripted" or memorized in
# some way.  For example, a common task in math class is to compute
# the length of the hypotenuse of a triangle.
#
#           |\
#           | \
#           |  \
#       x   |   \ hypot = sqrt(x**2 + y**2)
#           |    \
#           |_____\
#              y
#
# Mel has written out a list of "instructions" that carry out this
# operation, assuming that the values of "x" and "y" have already been
# entered. Could you give the `Calculator` class a "run" method that
# executes the instructions one after the other?  That is your task.

hypot = [             # Assumes "x" and "y" are already entered.
    ('push', 2),
    ('pow',),
    ('swap',),
    ('push', 2),
    ('pow',),
    ('add',),
    ('sqrt',)
]


class CalculateHypot(Calculator):

    def run(self, hypot):
        methods = {
            "push" : self.push,
            "pow": self.pow,
            "swap": self.swap,
            "add": self.add,
            "sqrt": self.sqrt
        }
        # method = getattr(self, op[0]) -> pythons dynamic behavior
        # for op in insturctions:
        #   method = getaddr(self, op[0])
        #   method(*op[1])
        # return

        for operation in hypot:
            method = methods[operation[0]]
            if len(operation) == 2:
                method(operation[1])
            else:
                method()

    def rul_sol(self, instructions):
        # python is slow because inside of it is a tiny stack machine
        # that runs your program, sort of like these statements below
        # bunch of instructions with if/else
        # def f(x, y, z): return x+y*z
        # import dis
        # dis.dis(f)
        # read the stack

        for op in instructions:
            if op[0] == "push":
                self.push(op[1])
            elif op[0] == "add":
                self.add()
            elif op[0] == "sub":
                self.sub()
            elif op[0] == 'mul':
                self.mul()
            elif op[0] == 'div':
                self.div()
            elif op[0] == "swap":
                self.swap()
            elif op[0] == "pow":
                self.pop()
            elif op == "sqrt":
                self.sqrt()
            else:
                raise RuntimeError()
                                                                                                                                                                                                                             


def test_hypot():
    calc = CalculateHypot()
    calc.push(3)
    calc.push(4)
    calc.run(hypot)             # <<< You need to implement this
    assert calc.pop() == 5.0
    print("Good script!")

# Uncomment
test_hypot()

# -----------------------------------------------------------------------------
# Exercise 9 - The Code Generator
#
# Everyone knows that normal people want to use standard math notation
# like 2 + 3 * 4.  Can't you make that work instead?"
# 
# Undeterred, you find out that Python has a standard library "ast" that
# can be used to parse expression strings into a tree data structure.
# From there, it's possible to generate stack instructions by walking the
# tree.  For example, suppose you have a tree node representing a
# binary operator like +:
#
#           BinOp
#          /  |   \
#      left   op   right
# 
# You can perform the calculation by imagining yourself at the calculator
# and thinking about the order of operations required:
#
#      push left
#      push right
#      op
#
# The following Python functions perform the conversion of Python AST trees
# to calculator instructions.   However, the generate_code() function is
# kind of messy.  Is there some way to improve upon that giant if-statement?
# -----------------------------------------------------------------------------
import ast

def generate_code(node, code):
    # Your challenge.  Can you come up with a better way of implementing this
    # giant if-statement? Note: This assumes the use of Python 3.8 or higher. 
    if isinstance(node, ast.Expression):
        generate_code(node.body, code)
    elif isinstance(node, ast.BinOp):
        generate_code(node.left, code)
        generate_code(node.right, code)
        generate_code(node.op, code)
    elif isinstance(node, ast.Add):
        code.append(('add',))      
    elif isinstance(node, ast.Sub):
        code.append(('sub',))
    elif isinstance(node, ast.Mult):
        code.append(('mul',))
    elif isinstance(node, ast.Div):
        code.append(('div',))
    elif isinstance(node, ast.Constant):
        code.append(('push', node.value))
    else:
        raise RuntimeError(f"Can't generate code for {node}")
    
def run_expression():
    tree = ast.parse("1.0 + (2 * (3 - (4 / (5 + (6 * (7 - (8 / 9)))))))", mode='eval')

    # Study this output
    print(ast.dump(tree))

    # Make instructions
    instructions = []
    generate_code(tree, instructions)
    
    # Run the instructions
    calc = Calculator()
    calc.run(instructions)
    print(calc.pop())

# Uncomment
# run_expression()




        

        
