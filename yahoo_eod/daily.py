#!/usr/bin/python

BATCH_SIZE = 50

import datetime
import os
import pickle
import time
import urllib

def floatify(x):
    if x == 'N/A': return None
    return float(x)

def floatify_kmb(x):
    if x == 'N/A': return None
    suffix = x[-1]
    return floatify(x[:-1]) * { 'T': 1000000000000, 'B' : 1000000000, 'M': 1000000, 'K': 1000 }[suffix]

def date1(x):
    if x == '"N/A"': return None
    ret = [int(x[1:-1].split("/")[i]) for i in (2,0,1)]
    if ret[0] < 1950 or ret[0] > 2020:
        raise ValueError("Year = %d out of range!" % ret[0])

    if ret[1] < 1 or ret[1] > 12:
        raise ValueError("Month = %d out of range!" % ret[1])

    if ret[2] < 1 or ret[2] > 31:
        raise ValueError("Day = %d out of range!" % ret[2])

    return datetime.date(ret[0], ret[1], ret[2])

def date2(x):
    if x == '"N/A"': return None
    v = x[1:-1].split("-")
    ret = (
        1900+int(v[2]),
        ['___', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(v[1]),
        int(v[0]),
    )

    if ret[0] < 1950 or ret[0] > 2020:
        raise ValueError("Year = %d out of range!" % ret[0])

    if ret[2] < 1 or ret[2] > 31:
        raise ValueError("Day = %d out of range!" % ret[2])

    return datetime.date(ret[0], ret[1], ret[2])
    
def date3(x):
    if x == '"N/A"': return None
    v = x[1:-1].split(' ')
    ret = (
        datetime.date.today().year,  ## FIXME: should be the year for which the following month/day has not arrived yet. Still a problem with same dates.
        ['___', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(v[0]),
        int(v[1]) )

    return datetime.date(ret[0], ret[1], ret[2])

def tryalldates(x):
    try:
        return date1(x)
    except Exception:
        pass

    try:
        return date2(x)
    except Exception:
        pass

    try:
        return date3(x)
    except Exception:
        pass

# Useful fields:                                  # example 1                 example 2  symbol description
fields = [
["s" , "symbol", lambda x:x],                     # "BRK-A"                   "AAPL"       s  - Symbol 
["b4", "book_value", floatify],                   # 90633.8906                52.175       b4 - Book Value
["d1", "last_trade_date", tryalldates],                 # "11/26/2010"              "11/26/2010" d1 - Last Trade Date
["e" , "earnings_per_share", floatify],           # 7226.5791                 15.154       e  - Earnings/Share 
["g" , "days_low", floatify],                     # 119118.25                 312.94       g  - Day's Low
["h" , "days_high", floatify],                    # 119750.00                              h  - Day's High
["j1", "market_capitalization", floatify_kmb],    # 197.2B                    289.0B       j1 - Market Capitalization
["o" , "open", floatify],                         # 119300.00                 313.55       o  - Open
["p" , "close", floatify],                        # 120500.00                 314.795      p  - Previous Close 
["q" , "ex_dividend_date", tryalldates],          # "N/A"                     "21-Nov-95"  q  - Ex-Dividend Date
["r" , "pe_ratio",floatify],                      # 16.67                     20.77        r  - P/E Ratio  
["r1", "dividend_date",tryalldates],              # "N/A"                     "N/A"        r1 - Dividend Pay Date
["v" , "volume",lambda x:int(x)],                 # 127                       8285258      v  - Volume
["d" , "dividend",floatify],                      # ??????????????????????????????         d  - Dividend per share
["e1", "error",lambda x:x],                       # "N/A"                     "N/A"        e1 - Error Indication (returned for symbol changed / invalid)
]
# "f6",                                           # 910,711,000    f6 - Float Shares (yes, they really return this value as unquoted commas)

functions_map = dict(zip((v[1] for v in fields), (v[2] for v in fields)))

stock_list = [ s.split("=")[0] for s in open("hkex.list", "r").read().strip().split("\n") ]

stuff = {}  # the place to put all the grabbed data to be dumped by pickle to a file

s = []   # this is not a clean solution, but I'll live with it.
for stock in stock_list:
    s.append(stock)
    if len(s) < BATCH_SIZE and stock != stock_list[-1]: continue

    u = urllib.urlopen('http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (",".join(s), "".join((v[0] for v in fields))))
    lines = u.read().strip().split("\n")

    if len(lines) != len(s):
        raise Exception("Unexpected number of lines returned")

    for line in lines:
        values = line.split(",")
        if len(values) != len(fields):
            raise Exception("Unexpected number of values on a line")

        data = {}

        raw_data = dict(zip((v[1] for v in fields), values))

        # try to parse the values
        for field in raw_data:
            try:
                data[field] = functions_map[field](raw_data[field])
            except Exception, e:
                raise ValueError("Cannot process field = %s with value = '%s'" % (field, raw_data[field]))

        stuff[data['symbol']] = data

    s = []
    time.sleep(3)

pickle.dump(stuff, open("dailydump/%s.pickle" % str(datetime.date.today()), "wb"), 2)
