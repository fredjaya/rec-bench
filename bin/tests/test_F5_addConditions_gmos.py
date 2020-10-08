#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:26:59 2020

@author: Fred Jaya
"""

import unittest

class testFunctions(unittest.TestCase):
    
    def setUp(self):
        self.newline = "\n"
        self.name = "-------------  mosaic structure : (2) FP7_037_T01_78925_2002.0877_194_28.2 -------------"
        self.query = "           1        1681	*        1681      6549.0	0.000000e+00	S2    	             "
   
    def test_check_line(self):
        self.assertEqual(
                check_line(self.newline),
                "newline")
        
        self.assertEqual(
                check_line(self.name),
                "query_name")
        
        self.assertEqual(
                check_line(self.query),
                "subject_mosaic")

if __name__ == '__main__':
    unittest.main()