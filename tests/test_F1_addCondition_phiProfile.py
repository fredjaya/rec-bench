#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon 4 Jan 2021

@author: Fred Jaya
"""

import unittest
import csv
import os
import re

from bin.F1_addCondition_phiProfile import get_significance, get_condition

class testPhiConditions(unittest.TestCase):

    def setUp(self):
        """
        Toy data
        """
    
    def test_get_significance(self):
        self.assertTrue(get_significance(0))
        self.assertTrue(get_significance(0.05))
        self.assertFalse(get_significance(0.051))

    def test_get_condition(self):
        self.assertEqual(get_condition(True, True), "TP")
        self.assertEqual(get_condition(False, True), "FP")
        self.assertEqual(get_condition(False, False), "TN")
        self.assertEqual(get_condition(True, False), "FN")

if __name__ == '__main__':
    unittest.main()
