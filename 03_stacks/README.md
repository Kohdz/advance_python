# Programming with Objects

Classes are sometimes used to define data.  However, classes are also
sometimes used to define behavior and programming interfaces.  This
project explores various facets of defining objects, relationships
between objects, designing for testability, and more.  We'll also peek
a bit inside the internal workings of an interpreter--incuding Python.

Go to the file `stacks.py` and follow the instructions inside.  The
file `calculator.py` is used for the second half of the project. Look
at that after you've finished with `stacks.py`.

The rest of the document provides some review of Python features
related to classes.

## Review of Classes

An object is defined by a `class` statement. For example:

```
class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# Example use
p = Player('Guido', 2, 3)
p.move(-1, 2)
print(p.x, p.y)    #  Prints 1 5
```

Defining an object is usually a straightforward process--
use the `class` statement, define an `__init__()` method to set
up some data, and define some methods as functions using `def`.
Don't forget to include the extra `self` argument which is a
variable that refers to an instance of the class.  In the
above example, an operation such as `p.move(-1, 2)` is the
same as `Player.move(p, -1, 2)`.  

## Customizing a Class

A core feature of object-oriented programming is that classes
can be customized.  A common way to do this is to use inheritance.
For example, maybe there is a `FastPlayer` class where movement
has been accelerated:

```
class FastPlayer(Player):
    def move(self, dx, dy):
        self.x += 2*dx
	self.y += 2*dy

# Example use
p = FastPlayer('Guido', 2, 3)
p.move(-1, 2)
print(p.x, p.y)   # Prints (0, 7)
```

If a redefine method is slight change to an existing method, it is
common to see `super()` used instead.  For example:

```
class FastPlayer(Player):
    def move(self, dx, dy):
        super().move(2*dx, 2*dy)
```

## Mixins

Sometimes code modifications can be implemented in a slightly different way.
For example, you can put the modified code in its own class like this, but
involving *no* inheritance:

```
class DoubleSpeed:
    def move(self, dx, dy):
        super().move(2*dx, 2*dy)
```

At first glance, that looks broken.  However, it's a fragment of code
that you could combine with an existing object:

```
class FastPlayer(DoubleSpeed, Player):
    pass
```

This is an example of something known as a "Mixin" class.  It's a
class that serves no useful purpose on its own, but can modify the
behavior of other existing classes.

## Interfaces

Sometimes different classes have a common behavior.  For example,
suppose you were making a game and there were also vehicles and
buildings:

```
class Vehicle:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
	self.y = y

    def move(self, dx, dy):
        self.x += dx
	self.y += dy

class Building:
    ...
```

Instances of `Player` and `Vehicle` are movable whereas `Building` is not.
You might want to express the the concept of a "behavior" in an abstract
way.  One way to do that is to define a class like this:

```
class Movable:
    def move(self, dx, dy):
        raise NotImplementedError()
```

This is not something that's meant to be used directly (what is an
instance of a "Movable" anyways). Instead, it's used to establish a
relationship with other classes.  This is done through inheritance:

```
class Player(Movable):
    ...
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    ...

class Vehicle(Movable):
    ...
    def move(self, dx, dy):
        self.x += dx
	self.y += dy
```

Such an inheritance relationship might be useful in programs that use
type-hints.

```
def update_position(m:Movable):
    ...
```

It can also be useful for performing run-time case-analysis.
For example:

```
if isinstance(p, Movable):
    p.move(dx, dy)
else:
    raise RuntimeError("Not movable!")
```

## getattr()

Another method that's sometimes used on a class is `getattr()`.  This
is sometimes used as an alternative mechanism of attribute lookup.
For example:

```
p = Player('Guido', 3, 4)
print(getattr(p, 'x'))   # -> 3
print(getattr(p, 'y'))   # -> 4

# Can also be used to access methods
getattr(p, 'move')(-1, 2)
```

There are some unusual uses for `getattr()` that get covered in later
parts of the project.


