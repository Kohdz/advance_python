# Owning Your Abstractions

As a programmer, it's common to define data structures--typically in
the form of a class.  In this exercise, we explore the interplay
between the use of classes and built-in data structures such as lists
and dicts.  The starting point for the project is `report.py`.  Go
there first to read about the project and follow the instructions found.

## Classes

Classes are often used to represent data. For example:
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
	self.height = height
```

or, if you prefer, you could write it using a dataclass:

```python
from dataclasses import dataclass

@dataclass
class Rectangle:
    width: int
    height: int
```

With classes, you have the option of adding methods.  For example, you
could add a method to compute the area:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
	self.height = height

    def area(self):
        return self.width * self.height
```

Here's a usage example:

```
>>> r = Rectangle(4, 5)
>>> r.width
4
>>> r.height
5
>>> r.area()
20
>>>
```

## Properties

For methods that take no arguments and return values, it sometimes common to define a property
like this:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
	self.height = height

    @property
    def area(self):
        return self.width * self.height
```

The main benefit of a property is that you don't need to add the extra parentheses.
For example:

```
>>> r = Rectangle(4, 5)
>>> r.width
4
>>> r.height
5
>>> r.area
20
>>>
```

This often gives a more consistent interface

## Containers

Programs also have to work with collections of objects.  For this,
you can use built-in objects such as lists and dictionaries.

```python
rectangles = [ Rectangle(10, 20), Rectangle(4, 5), Rectangle(2, 3) ]
```

You're not limited to the containers that Python provides.  If you
want, you can make a custom class that holds data. For example:

```python
class Shapes:
    def __init__(self):
        self._shapelist = [ ]

    def add_shape(self, shape):
        self._shapelist.append(shape)

    def __len__(self):
        return len(self._shapelist)

    def __iter__(self):
        return iter(self._shapelist)
```

If you're going to make a custom container, there are a few extra
methods that usually get defined.  First the `__len__()` method is
added to indicate how many items are part of the container.  Python
also uses this to determine truth-value testing. It is a common
convention for empty containers to evaluate as "false" in logic
checks.  This would be indicated by returning a length of 0 from
`__len__()`.  Second, the `__iter__()` method is used to create an
iterator for use with the for-loop.  Typically, you don't need to do
much in these extra methods.  It is common to forward the operation to
the corresponding operation on an internal data structure such as a
list or dict.

There are additional container methods that might get defined
depending on how fancy you want your container to be:

```python
a[index]            # a.__getitem__(index)
a[index] = value    # a.__setitem__(index, value)
del a[index]        # a.__delitem__(index)
x in a              # a.__contains__(x)
```



# Classes, Containers, and Data Abstraction

These three exercises build on each other to explore a central question in software design: **when should you wrap data in a class, and what should that class look like?**

---

## Exercise 1: Classes vs. Dictionaries

The first exercise replaces plain dictionaries with a `Holdings` class (implemented as a dataclass).

```python
# Before
holding = { 'name': name, 'shares': shares, 'price': price }

# After
@dataclass
class Holdings:
    name: str
    shares: int
    price: float

    def value(self):
        return self.shares * self.price
```

### Why bother?

A dictionary works fine, but a class gives you several things a dictionary can't:

**Identity and type.** The concept of a "stock holding" now has a name in your program. You can use it in type hints, and it's immediately clear what you're working with when reading the code.

**Cleaner syntax.** `h.name` reads more naturally than `h['name']`. It's a small thing, but it adds up across a large codebase.

**Attached behavior.** A dictionary is just data. A class lets you attach methods that naturally belong to the concept. A `value()` method (shares × price) is a great example — it's a computation that belongs to a holding, not scattered throughout your application code.

**Note on `@property` vs methods:** The code comments flag an important distinction. Marking `value` as a `@property` makes it look like a plain attribute (`h.value`), which is convenient but can hide the fact that computation is happening. For a simple multiplication this doesn't matter much, but for expensive computations, a method (`h.value()`) is more honest — it signals to the caller that *work* is being done.

---

## Exercise 2: Classes vs. Containers (the harder question)

The second exercise asks whether a plain Python list should be replaced with a `Portfolio` class. This is a subtler and more debated design question.

```python
class Portfolio:
    def __init__(self, holdings):
        self._holdings = holdings

    def __iter__(self):
        return iter(self._holdings)

    def sort_by_descending_value(self):
        self._holdings.sort(key=lambda h: h.value, reverse=True)

    def total_value(self):
        return sum(h.value for h in self._holdings)
```

### The core tradeoff

A list already does a lot. It iterates, it sorts, it indexes. So the question is: does wrapping it in a class actually add value, or just add complexity?

The answer depends entirely on *what interface you expose*. The exercises contrast two approaches:

**Bad Portfolio** — exposes Python internals:
```python
def sort(self, key=None, reverse=False):
    self._holdings.sort(key=key, reverse=reverse)
```
This doesn't improve anything. The caller still has to know the internal structure (passing a `lambda h: h.shares`, for example). You've added a wrapper with no benefit.

**Good Portfolio** — exposes application concepts:
```python
def sort_by_descending_value(self):
    self._holdings.sort(key=lambda h: h.value, reverse=True)
```
Now the caller doesn't need to know anything about the internal list. They just ask for what they want in domain terms. The implementation detail — that it's a sorted list, sorted by a lambda — is completely hidden.

### The rule of thumb

> If you're going to make a class, its methods should speak the language of your *application*, not the language of Python internals.

Methods like `sort_by_descending_value()` and `total_value()` are winners. A method that just re-exposes `list.sort()` is not.

### The `total_value` property trap

The code raises an important warning about properties that perform computation:

```python
# Looks like a simple attribute access, but runs a for-loop every time
for h in portfolio:
    print(f'{h.name}: {h.value * 100 / portfolio.total_value}%')
```

Here `portfolio.total_value` is called on every iteration of the loop, each time summing over all holdings. The property syntax hides this cost. A method name (`total_value()`) at least hints that something is being computed.

---

## Exercise 3: Data Abstraction and Dependency Inversion

The final exercise changes the internal representation of `Portfolio` from a Python list to a pandas DataFrame — *without changing the interface at all*.

```python
class PandasPortfolio:
    def __init__(self, df):
        self._df = df
        self._df['value'] = df['shares'] * df['price']

    def __iter__(self):
        for _, row in self._df.iterrows():
            yield Holdings(row['name'], row['shares'], row['price'])

    def sort_by_descending_value(self):
        self._df.sort_values('value', ascending=False, inplace=True)

    def total_value(self):
        return float(self._df['value'].sum())
```

The key insight: `report.py` doesn't need to change at all. It was written against the `Portfolio` interface, not against lists or pandas. Swapping the internals is entirely the Portfolio class's problem.

### Dependency Inversion

This is a formal design principle, and it's worth spelling out clearly.

Normally, your application code *depends* on a library (like pandas):

```
report.py  →  depends on  →  pandas
```

This is fragile. If you want to swap pandas for something else, you have to change `report.py` everywhere it touches pandas.

The better structure is to insert an interface layer:

```
report.py  →  depends on  →  Portfolio interface  ←  PandasPortfolio (uses pandas internally)
```

Now `report.py` depends on *your* abstraction, not on pandas. Pandas is an implementation detail of `PandasPortfolio`. If you want to replace pandas with Polars, or go back to a plain list, you only change one class — the rest of the application is untouched.

This is called **inversion** because you flip the dependency: instead of your application depending on a third-party library, the library integration depends on your interface.

---

## Summary

| Concept | Key Takeaway |
|---|---|
| Classes vs. Dicts | Classes give data an identity, cleaner syntax, and a home for related behavior |
| Classes vs. Containers | Only wrap a container in a class if you can expose an *application-focused* interface, not just a re-skin of the container |
| Data Abstraction | Write application code against an interface; hide implementation details inside the class |
| Dependency Inversion | Depend on abstractions you control, not on external libraries directly — makes it cheap to swap implementations |