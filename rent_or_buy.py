#!/usr/bin/python

from value import *

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You are permitted to use this software as long as you were legally given a copy
of the software. All other rights are expressly reserved.
"""

# For Hong Kong property market only.
### TODO:
# - Property tax not yet included.
# - "Rates" (chai heung) not included. Management fees not included.
# - Administrative costs not included.
### Other omissions might be here too.

############################################
# Calculate mortgage term given flat price, interests, and monthly payment
############################################
# For fixed monthly payment
# Ref: http://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula

my_yearly_interest = VARIABLE(0.02, "my interest")                  # this is the interest rate I can get from safe deposit/investments
bank_yearly_interest = VARIABLE(0.08, "bank interest")              # this is the interest my bank charges me
current_market_value_of_flat = VARIABLE(3000 * 600, "market value of flat now")  # for the flat to be purchased. Not necessarily same as the flat for rent.
property_avg_yearly_appreciation_rate_after_x_years = VARIABLE(0.02) # this is likely a wild guess, it should be safely set to be inflation rate
first_installment_budget = VARIABLE(30*10000, "first installment")  # money I have now to put into first installment
monthly_morgage_payment_budget = VARIABLE(15000, "monthly mortgage payment") # money I can pay monthly for morgage payments

principal_borrowed_from_bank = current_market_value_of_flat - first_installment_budget

print "I need to borrow", principal_borrowed_from_bank, "from bank."

mortgage_term_in_months = mortgage_fixed_payment_find_N(principal_borrowed_from_bank, bank_yearly_interest / 12, monthly_morgage_payment_budget)
mortgage_term_in_years = mortgage_term_in_months / 12

print "Mortgage term is", mortgage_term_in_years, "years."

############################################
# Present value of flat sold after n years #
############################################
# concept:
# a mortgage is a contract for a flat after N years if you pay $x every month for N years.
# so, I give: $x every month for N years
# I get: flat after N years

# cost to me
present_cost_of_morgage = present_value_of_annuity(monthly_morgage_payment_budget, mortgage_term_in_months, my_yearly_interest / 12)
print "Present cost of mortgage to me is:", present_cost_of_morgage

present_cost_of_buying_flat = present_cost_of_morgage + first_installment_budget
print "Present cost of buying flat (inc. first install):", present_cost_of_buying_flat

# present value of flat, using the "frying formula", i.e. assume property appreciation != interest rates I can get
future_value_of_flat_when_mortgage_ends = future_value_of_present_sum(current_market_value_of_flat, mortgage_term_in_years, property_avg_yearly_appreciation_rate_after_x_years)
present_value_of_flat_if_sold_right_after_mortgage = present_value_of_future_sum(future_value_of_flat_when_mortgage_ends, mortgage_term_in_years, my_yearly_interest)

# print "DEBUG, ", future_value_of_flat_when_mortgage_ends
print "Present value of flat if sold right after mortgage:", present_value_of_flat_if_sold_right_after_mortgage, "(not incl. value of having a home)"

############################################
# Utility value of having the purchased flat for n yrs
############################################
# XXX: this is one very subtle variable. This value depends on how the purchased flat is used.
# If used for rent, this should be the accumulated value of rent.  (i.e. market value of monthly rent * years * 12... no need to use annuity because rent can be increased, unless interest rates and rent rates differ a lot)
#                   Note: If we want to arbitrage the price diff between actual rent
#                   price and theoretical price, then put actual market price
#                   here, If we want to determine the theoretical rent value, this value should be adjusted so that net value of buying flat (final value below) is zero.

# If used as own home, this value should be the present value of utility of having a home for N years
# If used as own home, but I can live under worse conditions, then this value should be the rent of a flat I can minimally bear.

monthly_rent_of_flat = VARIABLE(7000, "monthly rent of flat (see comments!)")  # the value and subject of renting depends on how we want to use this variable.
present_utility_value_of_the_purchased_flat_for_n_years = mortgage_term_in_months * monthly_rent_of_flat

net_value_of_mortgaging = present_value_of_flat_if_sold_right_after_mortgage + present_utility_value_of_the_purchased_flat_for_n_years - present_cost_of_buying_flat

print "Net value of mortgaging:", net_value_of_mortgaging, "( don't buy flat now if negative! )"

## Print the values after N years for comparison
# print "INFO: Nominal total sum paid to bank over N years:", mortgage_term_in_months * monthly_morgage_payment_budget
# print "INFO: expected future nominal value of property after N years:", future_value_of_present_sum(current_market_value_of_flat, mortgage_term_in_years, property_avg_yearly_appreciation_rate_after_x_years)

