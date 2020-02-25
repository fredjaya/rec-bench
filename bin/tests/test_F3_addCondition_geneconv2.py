#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 18:38:02 2020

@author: Fred Jaya
"""

import unittest
import pandas as pd
from math import isnan

class TestGeneconvConditions(unittest.TestCase):
    
    def setUp(self):
        self.test_param = 'yes1'
        self.test_ser = pd.Series(['yes1', 'no2', 'no3'])
        self.test_nan = float('NaN')
        self.test_bp1 = '123:321:345'
        self.test_bp2 = '1'
        self.test_d   = pd.DataFrame({
                'params' : ['str1', 'str2', 'str3'],
                'seq'    : ['str1', 'str2', 'str3'],
                'breakpoints' : ['1', '123123','543']})
        self.test_set1 = {123, 324, 345} 

    def test_sim_in_gc(self):
        """ Test string matches a string in series"""
        self.assertEqual(
                sim_in_gc(self.test_param, self.test_ser), True)
    
    def test_match_breakpoints(self):
        """ NaNs and breakpoints parsed correctly """
        self.assertTrue(
                isnan(match_breakpoints(self.test_nan)))
        self.assertEqual(
                match_breakpoints(self.test_bp1), {123, 321, 345})
        self.assertEqual(
                match_breakpoints(self.test_bp2), {1})
    
    def test_bp_to_set(self):
        """ List output corresponds to index 
        
        Note - doesn't account for NaNs  
        """
        self.assertEqual(
                bp_to_set(self.test_d), [{1}, {123123}, {543}])
    
    def test_bp_length(self):
        self.assertEqual(
                bp_length(self.test_nan), 0)
        self.assertEqual(
                bp_length(self.test_set1), 3)
            
if __name__ == '__main__':
    unittest.main()
    