import math

# reference: http://en.wikipedia.org/wiki/Time_value_of_money

# a = Payment amount of each period
# n = number of time periods
# i = interest rate (1.00 = 100%)
def present_value_of_annuity(a,n,i):
    return 1.0 * a / i * ( 1.0 - ( 1.0 / (1.0 + i) ** n ) )

# a = payment amount of each period
# i = interest rate (1.00 = 100%)
def present_value_of_perpetuity(a,i):
    return 1.0 * a / i

# f = future value
# n = number of time periods
# i = interest rate (1.00 = 100%)
def present_value_of_future_sum(f,n,i):
    return 1.0 * f / ( (1.0 + i) ** n )

def future_value_of_present_sum(p,n,i):
    return 1.0 * p * ((1.0 + i) ** n)

# this is more of a annotation to indicate the meaning of a value, in this case, means this value is a variable, instead of a derived value.
def VARIABLE(a):
    return a


# c - payment amount per period (fixed)
# r - the interest rate per period
# N - the number of payments
# P - the amount borrowed, known as the loan's principal.

def mortgage_fixed_payment_find_N(P,r,c):
    try:
        return - ( math.log( 1.0 - ((1.0*r*P)/c) ) / math.log( 1.0 + r ) )
    except ValueError:
        raise "Payment rate not enough for mortgage of this size."
