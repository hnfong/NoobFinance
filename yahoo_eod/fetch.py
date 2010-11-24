#!/usr/bin/python

import urllib
import os
import time

hkex = open("hkex.list", "r").read().strip()

stocks = [ v.split("=")[0] for v in hkex.split("\n") ]

max_iterations = 1000

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
    try:
        f.write(urllib.urlopen(url).read())
    except KeyboardInterrupt:
        f.close()
        print "Removing ", filename
        os.unlink(filename)
        break
    f.close()

    os.system('git add "%s"; git commit -m "Data for %s"' % (filename, stock))

    time.sleep(3)

for stock in stocks:
    filename = "data/%s.div" % stock
    if os.path.exists(filename):
        print "%s already exists, skipping" % filename
        continue

    if max_iterations <= 0: break
    max_iterations = max_iterations - 1

    print "Fetching Dividend for: %s..." % stock
    f = open(filename, "w")
    url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&g=v' % stock
    try:
        f.write(urllib.urlopen(url).read())
    except KeyboardInterrupt:
        f.close()
        print "Removing ", filename
        os.unlink(filename)
        break
    f.close()

    os.system('git add "%s"; git commit -m "Data for %s"' % (filename, stock))

    time.sleep(1)
