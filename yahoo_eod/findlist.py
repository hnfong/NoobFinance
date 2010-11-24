#!/usr/bin/python

import urllib
import time
import re

### IMPORTANT ###
# Update these, otherwise the data will be out dated
valid_since_year = 2010
valid_since_month = 11
valid_since_day = 1

print "Note: We treat stocks that have traded since %d/%d/%d as valid."  % (valid_since_year, valid_since_month, valid_since_day)

def valid_date(v):
    # strip the double quotes
    if v[0] == '"' and v[-1] == '"':
        v = v[1:-1]

    m, d, y = [ int(k) for k in v.split("/") ]

    if y > valid_since_year: return True
    if y == valid_since_year and m > valid_since_month: return True
    if y == valid_since_year and m == valid_since_month and d >= valid_since_day : return True

    return False

f = open("hkex.list", "w")

# It seems to be warrants/cbcs after 9000.HK
for i in xrange(0, 90):
    s_string = "+".join( [ "%04d.HK" % k for k in range(i * 100 + 1, i * 100 + 101) ] )
    dat = urllib.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=snd1i" % s_string).read().strip()
    lines = dat.split("\r\n")
    if len(lines) != 100: raise Exception("Not 100 lines in output!")
    for line in lines:
        values = line.split(",")
        if len(values) != 4:
            raise Exception("Not 3 values in each line: " + line)

        # check whether the quote is valid, or is still actively trading
        if values[2] == '"N/A"' or not valid_date(values[2]) or values[0] == values[1]:
            continue

        # If "more information" is empty, probably not a stock (warrants, cbcs,
        # etfs, etc.).
        if values[3] == '""':
            print "not cepr or whatever for ", values

        f.write("%s=%s\n" % ( values[0][1:-1], values[1] ))
    time.sleep(1)

f.close()
