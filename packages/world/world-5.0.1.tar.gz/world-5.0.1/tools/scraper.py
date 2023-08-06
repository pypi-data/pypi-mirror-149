#!/usr/bin/python3

"""Very dumb scraper script to extract the latest ISO 3166 database.

In another blow to the open and free internet, ISO has once again put the
country code database behind a paywall.  The way to rebuild the database with
this script is to visit the following URL:

https://www.iso.org/obp/ui/#search

You have to enable JavaScript, and the select 300 results per page.  Since
there are only 249 entries (as of 2016-08-24), this will give you everything.
You cannot save that page because JavaScript.  Select All, then Copy, then
paste the results into a file.

If you're lucky, the file will mostly have the data, but it will be in a
horrible format.  There's a bunch of boilerplate at the top.  Delete that.
That should leave you with a file that contains the data starting with the
word "Afghanistan".  What should follow is a bunch of records, one per line of
the format:

    Country name in English
    Country name in French
    2-digit alpha code
    3-digit alpha code
    Numeric code

This script consumes that data and builds mapping dictionaries from one to the
other.  We currently only care about the English name, and the 2- and 3- digit
alpha codes.

This script isn't pretty because it doesn't need to be.  UTSL.
"""

import sys

from pickle import dump


data = []
expected = 249

with open(sys.argv[1], 'r', encoding='utf-8') as fp:
    # English, 2-digit code, 3-digit code
    while True:
        english = fp.readline().strip()
        french = fp.readline()
        two_digit = fp.readline().strip()
        three_digit = fp.readline().strip()
        numeric = fp.readline()
        if not all((english, french, two_digit, three_digit, numeric)):
            break
        data.append((english, two_digit, three_digit))
        print('[{}:{}] {}'.format(two_digit, three_digit, english))

if len(data) != expected:
    print('OOPS!  Expected {}, got {}'.format(expected, len(data)))


with open('src/world/data/codes.pck', 'wb') as fp:
    dump(data, fp)


sys.exit(0)
