#!/usr/bin/python

import urllib
import os
import time

hkex = open("hkex.list", "r").read().strip()

stocks = [ v.split("=")[0] for v in hkex.split("\n") ]

max_iterations = 100

for stock in stocks:
    filename = "data/%s" % stock
    if os.path.exists(filename):
        print "%s already exists, skipping" % filename
        continue

    if max_iterations <= 0: break
    max_iterations = max_iterations - 1

    print "Fetching: %s..." % stock
    f = open(filename, "w")
    url = 'http://ichart.finance.yahoo.com/table.csv?s=%s' % stock
    f.write(urllib.urlopen(url).read())
    f.close()

    os.system('git add "%s"; git commit -m "Data for %s"' % (filename, stock))

    time.sleep(3)
