#!/usr/bin/python

from value import *

yearly_interest = 0.02   # subject to change

v = 31                   # per day
i = yearly_interest/365  # interest per day
n = 365*10               # total 10 years

hospitalization_compensation = 900  # daily compensation for hospitalization

i_give = present_value_of_annuity(v, n, i)
i_get1 = present_value_of_future_sum(v*n, n, i)

print "i_give: ", i_give
print "i_get: ", i_get1
print "diff: ", i_give - i_get1
print "number of hospitalizations to best the contract: ", (i_give - i_get1)/hospitalization_compensation
print "present face value of total payments ", v*n

