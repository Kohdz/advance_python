"""theater.py

The owner of a monopolistic movie theater in a small town has
complete freedom in setting ticket prices.  The more he charges, the
fewer people can afford tickets.  The less he charges, the more it
costs to run a show because attendance goes up.  In a recent
experiment the owner determined a relationship between the price of
a ticket and average attendance.

At a price of $5.00/ticket, 120 people attend a performance.  For
each 10-cent change in the ticket price, the average attendance
changes by 15 people.  That is, if the owner charges $5.10, some 105
people attend on the average; if the price goes down to $4.90,
average attendance increases to 135.

Unfortunately, the increased attendance also comes at an increased
cost.  Every performance comes at a fixed cost of $180 to the owner
plus a variable cost of $0.04 per attendee.

The owner would like to know the exact relationship between profit
and ticket price in order to maximize the profit.

Write a program to figure out the best ticket price (to the nearest
10 cents) that maximizes profit.

Credit: This problem comes from "How to Design Programs", 2nd Ed.
"""


# a good engineer tests at the first sign of uncertainty 


# some comments
#     - I want to approach this as a software problem, not an algebra 
#     problem. Yes you could solve this specific problem using algebra
#     but programs are a bit different. For example, programs can be expanded
#     with new features. Maybe you want to be able to customize the problem. Maybe
#     your code is to be incorporated into a larger program of some kind

#   - the code should be broken into reasonable parts that can be tested and/or debugged
#     or atleast explained
# 
#   - Reabability counts. Could I give this code to others and have them understand it?
#     Could they modify it?
# 


# at $5.00 = 120 people
# .10+ -< +/- 15 people
# fixes = $180 + A*0.4

# best ticket price



# @@@@@@@@@@@@@@@@@@@@@@@@@@@ MY ATTEMPT @@@@@@@@@@@@@@@@@@@@@@@@@@@@


from decimal import Decimal

def best_ticket_price():
    initial_price = 5.00
    best_price = None
    max_profit = float("-inf")
    
    # Search wider range - maybe optimal is far from $5
    RANGE = 100  
    
    for i in range(RANGE):
        price_a = initial_price + (i * 0.10)
        attendees_a = 120 - (i * 15)
        
        price_b = initial_price - (i * 0.10)
        attendees_b = 120 + (i * 15)
        
        if attendees_a >= 0:
            cost_a = 180 + (attendees_a * 0.04)
            profit_a = (attendees_a * price_a) - cost_a
            
            if profit_a > max_profit:
                max_profit = profit_a
                best_price = price_a
        
        if attendees_b >= 0 and price_b >= 0:
            cost_b = 180 + (attendees_b * 0.04)
            profit_b = (attendees_b * price_b) - cost_b
            
            if profit_b > max_profit:
                max_profit = profit_b
                best_price = price_b
    
    return best_price, max_profit

# price, profit = best_ticket_price()
# print(f"Best price: ${price:.2f}")
# print(f"Max profit: ${profit:.2f}")

# print(best_ticket_price())
# assert print(best_ticket_price()) == 2.90

# @@@@@@@@@@@@@@@@@@@@@@@@@@@ Frame @@@@@@@@@@@@@@@@@@@@@@@@@@@@

# the place to start in a program: what are you trying to do in the program
# Nothing is said about how one might go about finding the best ticket price.
# Do we use a library? Is there a range of prices to check? Does the theater
# have a maximum capacity?

# Should I make the above values input parameters to find_ticket_price()?
def find_ticket_p():            # Wishful thinking (top-down approach)
    ...
    # but now what??
    ...


# @@@@@@@@@@@@@@@@@@@@@@@@@@@ Solution @@@@@@@@@@@@@@@@@@@@@@@@@@@@

from decimal import Decimal


BASE_PRICE = Decimal("5.0")               # Dollars
ATTENDEES_PER_DOLLAR =  Decimal("150")     # 150 people per dollar (15 people per 10 cents)
BASE_ATTENDEES =  Decimal("120")           # Number of attendees at base price
FIXED_COST =  Decimal("180.0")             # Dollars
COST_PER_ATTENDEE =  Decimal("0.04")       # Dollars

# Search parameters (which I'm making up on my own)
LOW_PRICE =  Decimal("1.0")
HIGH_PRICE =  Decimal("9.0")
INCREMENT =  Decimal("0.10")


def compute_attendees(price):
    return BASE_ATTENDEES - (price - BASE_PRICE) * ATTENDEES_PER_DOLLAR

def compute_cost(attendees):
    return FIXED_COST + COST_PER_ATTENDEE * attendees

def compute_profit(price):
    num_attendees = compute_attendees(price)
    revenue = num_attendees * price
    cost  = compute_cost(num_attendees)
    return revenue - cost

def find_ticket_price():  # Wishful thinking (top-down approach)
    price = LOW_PRICE
    best_price = price
    best_profit = compute_profit(price)

    while price < HIGH_PRICE:
        price += INCREMENT
        profit = compute_profit(price)
        if profit >= best_profit:
            best_price = price
            best_profit = profit

    return best_price

print(find_ticket_price())


""" What I am thinking about...

1. where do names go? 
    Only 3 places

    NAME = 'guido # Global
    def f(name)   # Function parameters

    class Example:  
        def __init__(self, name):
            self.name = name        # Class

2. the decomposition of the problem
    - have three functions, is that too many functions?


3. Nothing in the project had ranges; I made up the range of prices to check.
- consistency is important

4. who is the audience for the code?
"""

