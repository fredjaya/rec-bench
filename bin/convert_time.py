#!/usr/bin/env python3.7

import pandas as pd
import re
import numpy as np

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
