#!/usr/bin/env python3

import re
import datetime as dt

# Functions
def nf_timedelta(days, hours, mins):
    nf_time = dt.timedelta(days = days, hours = hours, minutes = mins)
    return nf_time

def nf_hours(t):
    t = str(t)
    total_hours = 0
    if re.findall('ms', t) == ['ms']:
            total_hours += 1/60 # minute
            
    else:
        if re.findall('d', t) == ['d']:
            days = re.findall('\d+(?=d)', t)
            total_hours += int(days[0]) * 24
            
        if re.findall('h', t) == ['h']:
            hours = re.findall('\d+(?=h)', t)
            total_hours += int(hours[0])
            
        if re.findall('m', t) == ['m']:
            mins = re.findall('\d+(?=m)', t)
            total_hours += int(mins[0]) / 60 
            
        if re.findall('s', t) == ['s']:
            total_hours += 1/60 # minute
            
    return(total_hours)
    
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

def test_nf_hours():
    assert nf_hours('1d') == 24, "Should be 24 hours"
    assert nf_hours('5h') == 5, "Should be 5 hours"
    assert nf_hours('1m') == 1/60, "Should be 1/60 hours"
    assert nf_hours('213234234s') == 1/60, "Should be 24 hours"
    assert nf_hours('1d 19h') == 43, "Error - %d%h doesn't add up"
    assert nf_hours('19h 30m') == 19.5, "Error - %h%m doesn't add up"
    assert nf_hours('3h 5s') == 3 + 1/60, "Error - %h%m doesn't add up"

    # calcs
    test_days = ['2']
    test_total_hours = 0
    test_total_hours += int(test_days[0]) * 24
    assert test_total_hours == 48, " error"

if __name__ == "__main__":
    test_nf_timeparse()
    test_seconds_to_hours()
    test_nf_hours()
    print("Everything passed")