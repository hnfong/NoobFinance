#!/usr/bin/python

from value import *

print "(Note: negative value are costs.)"

# variables
my_yearly_interest = VARIABLE(0.02)                # this is the interest rate I can get from safe deposit/investments
bank_yearly_interest = VARIABLE(0.04)              # this is the interest my bank charges me
number_of_years_of_renting = VARIABLE(10)
monthly_rent_of_flat = VARIABLE(9000)
current_price_of_flat = VARIABLE(3000 * 500)

first_installment = VARIABLE(0.3)                  # eg. 0.3 means 30% first installment

def value_of_n_years_rent_():
    # this period is one month
    n = number_of_years_of_renting * 12
    my_i = my_yearly_interest / 12
    a = monthly_rent_of_flat
    return present_value_of_annuity(a,n,my_i)
value_of_n_years_rent = value_of_n_years_rent_()

print "Current value of", number_of_years_of_renting , "years of rent:", value_of_n_years_rent

