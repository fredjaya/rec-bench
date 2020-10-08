#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:49:13 2020

@author: Fred Jaya
"""

import unittest
import csv
import os
import re

class testFunctions(unittest.TestCase):

    def setUp(self):
        """Toy data (simulated breakpoints)  """
        self.singleBP = {"bps": "888"}
        self.multiBP  = {"bps": "888:888:888:888:888"}
        self.bigBP    = {"bps": "1:2:2:3:3:3:4:4:4:4:5:5:5:5:5:157"}
            
    def test_get_sim_BP_counts(self):
        """Single bp  """
        self.assertEqual(
                get_sim_BP_counts(self.singleBP),
                {0: {'bps': 888, 'count': 1}})
        
        """Multi bp  
        
        Multiple occurrences of the same breakpoint  
        """
        self.assertEqual(
                get_sim_BP_counts(self.multiBP),
                {0: {'bps': 888, 'count': 5}})
        
        """Assorted multi BPs """
        self.assertEqual(
                get_sim_BP_counts(self.bigBP),
                {0: {'bps': 3, 'count': 3},
                 1: {'bps': 2, 'count': 2},
                 2: {'bps': 4, 'count': 4},
                 3: {'bps': 157, 'count': 1},
                 4: {'bps': 1, 'count': 1},
                 5: {'bps': 5, 'count': 5}})
    
if __name__ == '__main__':
    unittest.main()