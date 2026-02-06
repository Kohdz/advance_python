Notice how he is asserting at the first point of uncertinity
The moment he has an issue, tests each function in the IDE

To get into the ide, type `python -i name.py`

![ide](assets/ide.png)

John Ousterhout
- Working code isent enough: must minimize complexity
- Complexity comes from dependencies and obsecurity
- Strategic vs Tactical Programming
- Classes should be deep
- General-purpose classes are deeper
- New layer, new abstraction
- Comments should describe things that are not obvius from code
- Define errors out of existance
- Pull Complexity downwads

Classes should be deep
![](/assets/deep_classes.png)

Define errors out of existance

Throwing alot of exceptions is great!!!
explosion of exceptions that create bugs themslves

Redefine algorithm so you dont need the exception
When you should throw exceptions:
    - when you fundamentally cant carry out your contract with your caller
    - if you cant implement your interface you have to throw exception
    - your doing a read operation and you get an error because
    - you cant read file, etc

Tactical Tarnado: produces code that 80% works
Bad mindset to be like, "it works"
Leaves a mess behind them
I am a tactical Tarnado


Stragetic Programmer! Design Programmer
Design matters more (Concepts!; Garbage Can)
Sweat the small stuff


ASK: AM I DOING THE MOST I CAN? IF I WAS IMPLEMETING IT TODAY
WOULD IT LOOK LIKE THIS?

Person who has done the same job multiple time,
ask them, why haven't you moved on?

Good designer can go from implementation needs to user needs
empathy


Somme design; have a hypothesis
Redesign when you run into the problem

Get Better At Software Design


Names: Content (Protos) and Form/Shape (Zerg)
- Methods that do more than they
- Methods that say less than they say
- Methods that Reverse what they say

There are all names molds
max-monthly-order
monthly-max-order
order-month-max

As a team agree on molds

https://cep.dev/posts/design-better-software-abstractions-using-bipartite-composition/

Eric Normand distinguishes defining a function from implementing a function in software


https://6826.csail.mit.edu/2017/coqdoc/POCS.Spec.Abstraction.html


Day 1 - A Abstraction Layers
- Programming to an interface
- Gives flexibility to change your mind
- Can better isolate dependencies
- Programming in the "problem space" vs. Programming in the "Python space"

you generally want to be in the problem space and
not python space; abstraction helps you be in the problem
space

![](problem_vs_python.png)



Day 2 - Objects
- Programming with Classes
  1. code organization tool: put related things together
    in a common space
  2. Customization via inheritance
  3. attach to data (instances, __init__)
- Object-oriented programming
  - mindet that the world consists of objects (reality)
  - objects have state (data) (they exist, etc)
  - objects can be manipulated (via methods)
  - Manipulated => Mutation. (same object, different state)
  - push a button on toster still keeps it the same object
- but the state is mutated
  - Composition -> big objects are made up of smaller objects (car is made of wheels)
  - Subsitition -> any component can be replaced yb aa compitable substitute
  (same interface, same purpose)


// simmilar to a module
class MathOps:
    def add(x, y): return x + y
    def sub(x, y): return x - y
    def twice(x): return MathOps.add(x, x) (using MathOps. is bad) // better to do cls.add(x, x)
    // whole thing about classes are because they
    // are customizable

// module
import math
math.sqrt(2)


how python links data to methods or behavior
under the hood there is a dict, that stores the data

e = Example(2, 3)
e.__dict__
{'x': 2, 'y': 3}
e.__class__

e.x == e.__dict__['x']

e.method(10)
e.__class__.method



# Example of OO: list has data, you do something, list mututates
items = [1, 2, 3]
items.append(23)
items = [1, 2, 3, 23]

# Example of not OO: Strings
strings dont mutate, you make a copy and create a new one

