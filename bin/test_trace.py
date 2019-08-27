#!/usr/bin/env python3

import re
import datetime as dt

# Functions
def nf_timedelta(days, hours, mins):
    nf_time = dt.timedelta(days = days, hours = hours, minutes = mins)
    return nf_time

# Assertions
def test_nf_timeparse():
    # Check that query matches for ifelse statement
    test_str = '1d 19h 58m 36s'
    test_match = re.findall('d', test_str)
    assert test_match == ['d'], "should match ['d']"
    
def test_seconds_to_hours():
    test_td = nf_timedelta(days = 1, hours = 1, mins = 30)
    test_hours = test_td.total_seconds() / 60 / 60
    assert test_hours == 25.5, 'should be 25.5 hours'

if __name__ == "__main__":
    test_nf_timeparse()
    print("Everything passed")