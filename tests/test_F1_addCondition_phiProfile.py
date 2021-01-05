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

from bin.F1_addCondition_phiProfile import get_significance, get_condition, check_simbp_in_window, iterate_bp

class testPhiConditions(unittest.TestCase):

    def setUp(self):
        """
        Toy data
        """
        self.breakpoints = [1, 999, 1000, 3000]

    def test_get_significance(self):
        self.assertTrue(get_significance(0))
        self.assertTrue(get_significance(0.05))
        self.assertFalse(get_significance(0.051))

    def test_get_condition(self):
        self.assertEqual(get_condition(True, True), "TP")
        self.assertEqual(get_condition(False, True), "FP")
        self.assertEqual(get_condition(False, False), "TN")
        self.assertEqual(get_condition(True, False), "FN")

    def test_check_simbp_in_window(self):
        # Assuming window sizes == 1000 nt 
        self.assertTrue(check_simbp_in_window(500, 1000))
        self.assertTrue(check_simbp_in_window(500, 1))
        self.assertFalse(check_simbp_in_window(500, 0))
        self.assertFalse(check_simbp_in_window(500, 1001))

    def test_iterate_bp(self):
        # Assuming window sizes == 1000 nt 
        self.assertTrue(iterate_bp(500, self.breakpoints))
        self.assertFalse(iterate_bp(5000, self.breakpoints))
        self.assertFalse(iterate_bp(1500, self.breakpoints))

if __name__ == '__main__':
    unittest.main()
