#!/usr/bin/python

from value import *

print "(Note: negative value are costs.)"

############################################
# Value of N years rent                    #
############################################
# variables
my_yearly_interest = VARIABLE(0.02)                # this is the interest rate I can get from safe deposit/investments
number_of_years_of_renting = VARIABLE(10)
monthly_rent_of_flat = VARIABLE(9000)


def value_of_n_years_rent_():
    # this period is one month
    n = number_of_years_of_renting * 12
    my_i = my_yearly_interest / 12
    a = monthly_rent_of_flat
    return present_value_of_annuity(a,n,my_i)
value_of_n_years_rent = value_of_n_years_rent_()

print "Current value of", number_of_years_of_renting , "years of rent:", value_of_n_years_rent



############################################
# Utility value of having a home for n yrs #
############################################
# XXX: this is one very bad way of doing things....
# btw, may be able to somehow be derived...? or just set it equal to the best rent I can get?
utility_of_living_for_n_years = VARIABLE(978117)

print "My utility for having a home for", number_of_years_of_renting, "years: ", utility_of_living_for_n_years
print "Net value to me, renting a home for", number_of_years_of_renting, "years: ", utility_of_living_for_n_years - value_of_n_years_rent


############################################
# Present value of flat sold after n years #
############################################
# For fixed monthly payment
# Ref: http://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula

bank_yearly_interest = VARIABLE(0.07)              # this is the interest my bank charges me
current_price_of_flat = VARIABLE(3000 * 600)       # this value should refer to market value of same flat as the rent for meaningful comparison
property_avg_yearly_appreciation_rate_after_x_years = VARIABLE(0.02) # this is likely a wild guess
first_installment_budget = VARIABLE(30*10000)      # money I have now to put into first installment
monthly_morgage_payment_budget = VARIABLE(20000)   # money I can pay monthly for morgage payments

principal_borrowed_from_bank = current_price_of_flat - first_installment_budget

print "Property current nominal price:", current_price_of_flat

print "I need to borrow", principal_borrowed_from_bank, "from bank."

mortgage_term_in_months = mortgage_fixed_payment_find_N(principal_borrowed_from_bank, bank_yearly_interest / 12, monthly_morgage_payment_budget)
mortgage_term_in_years = mortgage_term_in_months / 12

print "Mortgage term is", mortgage_term_in_years, "years."

# concept:
# a mortgage is a contract for a flat after N years if you pay $x every month for N years.
# so, I give: $x every month for N years
# I get: flat after N years

# cost to me
present_cost_of_morgage = present_value_of_annuity(monthly_morgage_payment_budget, mortgage_term_in_months, my_yearly_interest)
print "Present cost of mortgage to me is:", present_cost_of_morgage

present_cost_of_buying_flat = present_cost_of_morgage + first_installment_budget
print "Present cost of buying flat (inc. first install):", present_cost_of_buying_flat

## DEBUG: Above seems correct.
print 
## DEBUG: below seems incorrect.

# present value of flat
future_value_of_flat_when_mortgage_ends = future_value_of_present_sum(current_price_of_flat, mortgage_term_in_years, property_avg_yearly_appreciation_rate_after_x_years)
print "DEBUG, ", future_value_of_flat_when_mortgage_ends

present_value_of_flat = present_value_of_future_sum(future_value_of_flat_when_mortgage_ends, mortgage_term_in_years, my_yearly_interest)
print "Present value of flat:", present_value_of_flat         # XXX: TODO: understand how this value relates to my_interest and property_appreciation!!!!!!!





# print "DEBUG: Total nominal sum paid to bank", monthly_morgage_payment_budget * mortgage_term_in_months

#future_nominal_value_of_flat_after_n_years = future_value_of_present_sum(current_price_of_flat, number_of_years_of_renting, property_yearly_appreciation_rate)
#present_value_of_flat_after_n_years = present_value_of_future_sum(future_nominal_value_of_flat_after_n_years, number_of_years_of_renting, my_yearly_interest)

# print "current value of buying outright, and selling after", : ", present_value_of_flat_after_n_years - cost_of_buying_outright
