# report.py
#
# Ben has decided to write some Python code to manage his stock
# portfolio. The file "portfolio.csv" is a CSV file containing some
# information about his stock holdings (name, number of shares,
# price).  The following program reads this file, sorts it, and prints
# out a small report.
#
# The module `portfolio.py` contains code for reading the data
# and returning it back as a list of dictionaries.  Take a few
# moments to run the program and look at the code.
#
# Upon showing this program to his co-workers, Ben is immediately
# accosted by his decision to directly use Python data structures
# such as dicts and lists.  "You should really use some classes
# or something man" noted Peter.
#
# Your task in this project is to explore this central question:
# Should you use custom classes to provide a kind of data abstraction
# layer or is it perfectly fine to use dictionaries and lists?
# If classes are used, what should they look like?
#
# Most of your work will take place in the `portfolio.py` file.  You
# will make a few minor code modifications here, but the code in
# this file should keep its original organization (i.e., you'll keep
# the make_report() and main() functions).
#
# Continue to `portfolio.py` to start the project.

import portfolio


def make_report(portfolio):
    '''
    Print a report
    '''
    portfolio.sort(key=lambda h: h['shares']*h['price'], reverse=True)
    print('{:>10} {:>10} {:>10} {:>10}'.format('name','shares','price','value'))
    print(('-'*10 + ' ')*4)
    total_value = 0.0
    for holding in portfolio:
        value = holding['shares']*holding['price']
        total_value += value
        print(f'{holding["name"]:>10s} {holding["shares"]:10d} {holding["price"]:10.2f} {value:10.2f}')

    print()
    print(f'Total value: {total_value:0.2f}')


def make_report_dataclass(portfolio):
    '''
    Print a report
    '''
    portfolio.sort(key=lambda h: h.shares*h.price, reverse=True)
    print('{:>10} {:>10} {:>10} {:>10}'.format('name','shares','price','value'))
    print(('-'*10 + ' ')*4)
    total_value = 0.0
    for holding in portfolio:
        value = holding.shares*holding.price
        total_value += value
        print(f'{holding.name:>10s} {holding.shares:10d} {holding.price:10.2f} {value:10.2f}')

    print()
    print(f'Total value: {total_value:0.2f}')



def make_report_class_proflio(portfolio: portfolio.Profilio2):
    '''
    Print a report
    '''
    # Discussion: This sorting operation is weird. As a list,
    # short() performs an in-place mutation. Is that what we want to be doing here?
    # If we're going to make a custom Portfolio class, this is something we could
    # # contemplate--do we allow mutation of the data or not? 
    #
    # Also, the key=lambda h:h value is part of exposing internal
    # implementation. Is sorting a core feature of portfolios or is it
    # a feature of making a report?

    portfolio._holdings.sort(key=lambda h: h.shares*h.price, reverse=True)
    print('{:>10} {:>10} {:>10} {:>10}'.format('name','shares','price','value'))
    print(('-'*10 + ' ')*4)
    total_value = 0.0
    for holding in portfolio:
        value = holding.shares*holding.price
        total_value += value
        print(f'{holding.name:>10s} {holding.shares:10d} {holding.price:10.2f} {value:10.2f}')

    print()
    print(f'Total value: {total_value:0.2f}')


def make_report_dataclass_proflio_2(portfolio: portfolio.Profilio2):
    '''
    Print a report
    '''
    portfolio.holdings.sort(key=lambda h: h.shares*h.price, reverse=True)
    print('{:>10} {:>10} {:>10} {:>10}'.format('name','shares','price','value'))
    print(('-'*10 + ' ')*4)
    total_value = 0.0
    for holding in portfolio:
        value = holding.shares*holding.price
        total_value += value
        print(f'{holding.name:>10s} {holding.shares:10d} {holding.price:10.2f} {value:10.2f}')

    print()
    print(f'Total value: {total_value:0.2f}')





def main(filename):
    port = portfolio.read_portfolio(filename)
    make_report(port)
    
if __name__ == '__main__':
    main('portfolio.csv')
