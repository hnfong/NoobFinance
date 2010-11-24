import glob
import os
import sqlite3

# we can afford to rebuild the database every time as long as it's not too often....
try:
    os.unlink('data/hk.sqlite3')
except OSError:
    pass

conn = sqlite3.connect('data/hk.sqlite3')

conn.execute("""
    CREATE TABLE EndOfDayData (
        symbol VARCHAR,
        day DATE,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume INTEGER,
        adj_close FLOAT,
        PRIMARY KEY(symbol, day) ON CONFLICT REPLACE
    );""")  ## TODO: add indexes

conn.execute("""
    CREATE TABLE FailedQuotes (
        symbol VARCHAR
    );""")

for infile in glob.glob(os.path.join('data', '*.HK')):
    lines = open(infile, "r").read().strip().split("\n")
    symbol_ = infile[5:-3]

    if lines[0] != 'Date,Open,High,Low,Close,Volume,Adj Close':
        conn.execute("INSERT INTO FailedQuotes VALUES(?)", ( symbol_, ))
        continue

    lines = lines[1:]
    print "importing from %s as \"%s\"" % (infile, symbol_)
    for line in lines:
        try:
            date_, open_, high_, low_, close_, volume_, adj_ = line.split(",")
        except Exception:
            raise "error reading: ", infile

        conn.execute("INSERT INTO EndOfDayData VALUES(?, ?, ?, ?, ?, ?, ?, ?)", ( symbol_, date_, open_, high_, low_, close_, volume_, adj_))

conn.commit()
