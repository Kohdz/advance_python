# portfolio.py
#
# This file contains a function that reads a CSV file of
# "name,shares,price" data into a list of dictionaries.  The file
# `report.py` uses this function.   We'll make some modifications
# in exercises below.

from dataclasses import dataclass

def read_portfolio(filename):
    '''
    Read a CSV file of name, shares, price data into a list of dicts.
    '''
    portfolio = [ ]
    with open(filename, "r") as file:
        # Skip the first line of headers
        next(file)
        for line in file:
            row = line.split(',')
            name = row[0]
            shares = int(row[1])
            price = float(row[2])
            holding = { 'name': name, 'shares': shares, 'price': price }
            portfolio.append(holding)
    return portfolio

# -----------------------------------------------------------------------------
# Exercise 1:  Classes vs. Dicts
#
# In the above code, a dictionary is used to represent a single record of
# data.  For example, in the line:
#
#          holding = { 'name': name, 'shares': shares, 'price': price }
#
# Instead of using a dictionary, what if you used a class instance?
# What core features would you give this new class?
#
# You first task is as follows:
#
#     1. Define a class to replace the holding dictionary.
#     2. Write a new version of read_portfolio() that uses this class.
#     3. Modify report.py as necessary to work with instances.
#
# Are there any parts of the `report.py` program that could be better
# organized as features of this newly defined class instead?  For
# example, should the class have any methods added to it?
# 
# Some Thoughts:
#   1. Gives the concept of stock holding a name (Holding)
#   2. Potentially useful if one were to include it in type hints
#   3. Less 'fiddly' syntax. h.name vs h['name]
#   4. Could also include common functionality (e.g value computation)
#   5. could use `holding.value()`

@dataclass
class Holdings:
    name: str
    shares: int
    price: int

    # @property # does not allow you to use `value()`
    def values(self):
        return self.shares * self.prices


def read_portfolio2(filename):
    '''
    Read a CSV file of name, shares, price data into a dataclass.
    '''
    portfolio = [ ]
    with open(filename, "r") as file:
        # Skip the first line of headers
        next(file)
        for line in file:
            row = line.split(',')
            name = row[0]
            shares = int(row[1])
            price = float(row[2])
            portfolio.append(Holdings(name=name, shares=shares, price=price))
    return portfolio

# -----------------------------------------------------------------------------
# Exercise 2:  Classes vs. Containers
#
# In this code, a Python list is being used to represent a "Portfolio"
# of stock holdings.   Does it make any sense to use a custom Portfolio
# class for this instead?  If so, what would that class look like and
# what features should it support?
#
# Your task is as follows:
#
#    1. Define a Portfolio class that takes the place of a Python list.
#    2. Write a new version of read_portfolio() that creates this class.
#    3. Modify report.py as necessary to work with the data.
#
# Are there any parts of the `report.py` program could be better
# organized as features of the `Portfolio` class instead?  Note:
# we're going to keep the make_report() function separate.  That
# should NOT turn into a method.


# Protfolio hides its internal data completely
# and only exposes selected functionality through methods
class Portfolio:
    def __init__(self, holdings):
        self._holdings = holdings

    def __iter__(self):
        return iter(self._holdings)

    # The report wants to sort... do I just "copy" the
    # list sort operation here?  I dont like this because it exposed
    # internal details via the required key function
    def sort(self, key=None, reverse=False):
        self._holdings.sort(key=key, reverse=reverse)

    # Do I make a completely new sorting method that hides details?
    # Pro: doesent expose internal details. Mabye convient to user
    def sort_by_descending_value(self):
        self._holdings.sort(key=lambda h: h.value, reverse =True)


    # Maybe I do nothing-sorting is someones else's problem
    # If someone else's problem, the they're going to have to copy
    # the data into their own format and sort it on their own


    # Some thoughts... I'm not sure I would expose the internal list via a property
    # Partly because the property doesn't seem to do very much as all. If it was 
    # important to see the internal list, I might make it a public attribute (no undersore)
    # instead
    @property
    def holdings(self):
        return self._holdings
    

    # What is the boundary between a property and method? One dander with properties that
    # perform computation is that it might be unclear to a user that access to some attribute like
    # `port.total_value` is actually performing a for-loop over all the data each time.
    # This can be a way to accidentally introduce alot of extra computation.
    # As an example, conside this loop that prints out the portion of each holding as a precent:
    # 
    # for h in portfolio:
    #     print(f'{h.name}: {h.value*100/portfolio.total_value}%')
    # 
    # `portfolio.total_value` in that loop is not an attribute, but it's a 
    # computation over the data involving its own for-loop
    @property
    def total_value(self):
        return sum(h.shares * h.price for h in self)


# Commentary: I think if you're going to introduce a Portfolio class,
# the purpose of doing so should be in some kind of service to the application
# The methods should be primarily related to the application,
# not python (internals). Thus almost all fo the methods should be focused
# on application-specific needs (e.g sort_by_descending_value() is the winner)





# One possibility: Portfolio is purely data. Maybe we defien it as a
# dataclass just like Holding

@dataclass
class Profilio2:
    holdings: list[Holdings]

# Comments: Aside from giving Portfolio some kind of identity as 
# type, this doesn't seem like its giving anything more than a list
# is already providing


def read_portfolio_profilio_2(filename):
    '''
    Read a CSV file of name, shares, price data into a dataclass.
    '''
    holdings = [ ]
    with open(filename, "r") as file:
        # Skip the first line of headers
        next(file)
        for line in file:
            row = line.split(',')
            name = row[0]
            shares = int(row[1])
            price = float(row[2])
            holdings.append(Holdings(name=name, shares=shares, price=price))
    return Profilio2(holdings)



# Correct Portfolio
class PortfolioCorrect:
    def __init__(self, holdings):
        self._holdings = holdings

    def __iter__(self):
        return iter(self._holdings)

    def sort_by_descending_vaue(self):
        self._holdings.sort(key=lambda h: h.value, reverse=True)

    def total_value(self):
        return sum(h.value for h in self._holdings)
    
# Commentary: If above Portfolio class is written with an application focus--
# it is much easier to change the internal data representaion



# -----------------------------------------------------------------------------
# Exercise 3: Data Abstraction
#
# A core tenant of data abstraction is that applications are written to
# a specific programming interface and that internal implementation details
# don't matter so much.   Think about all of the different ways that
# fractions were implemented in Project 1.
#
# Suppose that you wanted to change the internal representation of data
# inside your Portfolio class to use pandas.   Pandas has a helpful function
# for reading a CSV file:
#
#       import pandas
#       data = pandas.read_csv('portfolio.csv')
#
# What modifications would you make to the Portfolio class to use
# pandas dataframes as an internal data representation format?
#
# Can you use the modified Portfolio class with the `report.py`
# program *WITHOUT* making any changes to the code in that file?
#
# Note: For this exercise, it make might sense to make a separate
# class PandasPortfolio.   Keep in mind that an instance of this class
# would be provided to the make_report() function in report.py.

# you just change from a list -> pandas dataframe. 
# The rest of the code should be the same
# changed the internals, but interface is the same, 
# so report.py should work without modification
class PandasPortfolio:
    def __init__(self, df):
        self._df = df # Pandas dataframe
        # Add a value column
        self._df['value'] = df['shares'] * df['price']


    # Same interface as Portfolio, but internal data stored in pandas.
    def __iter__(self):
        # This must produce Holding instance for compatibility with Portfolio
        for _, row in self.df.iterrows():
            yield Holdings(row['name'], row['Share'], row['price'])

    def sort_by_descending_value(self):
        self._df.sort_values('value', ascending=False, inplace=True)

    def total_value(self):
        return float(self._df['value'].sum())


class Pandas:
    def __init__(self):
        pass

    
    def read_csv(self, filename):
        pass

def read_portfolio_pandas(filename):
    return PandasPortfolio(Pandas.read_csv(filename))


# Overall: Lists are great! Not sure I would make a class out of Portfolio.
# Only reason I would is if I wanted to hide internal details and provide a more
# application-focused interface.
# I dont want to think about lists, but want to think about portfolios. 
# If I make a Portfolio class, I can hide the list details and just give 
# users the features they care about (e.g sorting by value, total value, etc).
#  If I just use a list, then users have to know how to do those things on 
# their own.

# By hiding internals, look at the methods of Portfolio
# Nothing for `add_holdings` or `sort_by_descending_value` give away that
# it uses a list internally; iterator is alittle suggestive

# Another issue to consider: Imagine you have an application with depenecies
# depencies with Pandas. Imagine you continually call pandas
# one school of though says that you should not do that. You should
# create an interface, (what we are doing with Portfolio)
# the you write your application on that
# the thinking is if you want to ditch from Panadas, you can do that by just
# changing the interface layer (Dependency Inversion)
# Its called inversion, because inverts from depending on something to depending
# on your stuff!!!!!