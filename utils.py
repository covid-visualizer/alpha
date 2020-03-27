"""
Miscellaneous routines related to days.

This software is in the public domain.
"""

import datetime

TODAY = datetime.datetime.now()
TODAY_STRING = TODAY.strftime( '%d %B' )

# Base day is the "today" in the graphs, against which previous-day offsets are computed.
BASE_DAY = TODAY
BASE_DAY_STRING = BASE_DAY.strftime( '%d %B' )
print('Base day =', BASE_DAY_STRING)

def day_of_year( month, day ):
    return int( datetime.date( BASE_DAY.year, month, day ).strftime('%j') )

BASE_DAY_DAYOFYEAR = day_of_year( BASE_DAY.month, BASE_DAY.day )

def is_date_spec( s, *x ):
    try:
        month, day = list(map( int, s.split('--') ))
        #print 8084, month, day
        return ( month, day )
    except:
        return False

def offset_string( offset ):
    offset_day = BASE_DAY + datetime.timedelta( offset )
    return offset_day.strftime( '%d%b' )
