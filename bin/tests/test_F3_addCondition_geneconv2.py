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
        self.test_nan = float('NaN')
        self.test_bp1 = '123:321:345'
        self.test_bp2 = '1'
        self.test_d   = pd.DataFrame({
                'params' : ['str1', 'str2', 'str3'],
                'seq'    : ['str1', 'str2', 'str3'],
                'breakpoints' : ['1', '123123','543']})
    
        self.test_set_sim = {111, 222, 333} 
        self.test_set_gc = {111, 222, 444, 555, 666}
        
        """ Sim yes gc yes (matches gcser1) """
        self.test_simrow1 = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.0010_rc0.0010_n100_dual0.25_rep2.tab',
                 'seq_11',
                 {111, 222, 333, 666}],
                 index = ['params', 'seq', 'breakpoints'])
        
        """ Sim yes gc no """
        self.test_simrow2 = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.000010_rc0.00010_n5000_dual1_rep3.tab',
                 'seq_999',
                 {111, 999, 888}],
                 index = ['params', 'seq', 'breakpoints'])
        """ Sim no gc no """
        self.test_simrow3 = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.0010_rc0.000010_n5000_dual0.1_rep3.tab',
                 'seq_666',
                 float('NaN')],
                 index = ['params', 'seq', 'breakpoints'])
        """ Sim no gc yes """
        self.test_simrow4 = pd.Series(        
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.0010_rc0.000010_n5000_dual0.1_rep3.tab',
                 'seq_80',
                 float('NaN')],
                 index = ['params', 'seq', 'breakpoints'])
        
        self.test_sim_bp = pd.DataFrame(
                columns = ['params', 'seq', 'breakpoints'])
        self.test_sim_bp.loc[0] = self.test_simrow1
        self.test_sim_bp.loc[1] = self.test_simrow2
        
        """ sim yes gc yes (matches simrow1) """
        self.test_gc_ser1 = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.0010_rc0.0010_n100_dual0.25_rep2.tab',
                 1e-03, 1e-03, 100, 0.25, 2, 'seq_11', {111, 222, 99, 88}],
                 index = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])  
        self.test_gc_ser2 = pd.Series(    
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.00010_rc0.00010_n1000_dual0.5_rep2.tab',
                 1e-04, 1e-04, 1000, 0.5, 2, 'seq_200', {111, 222, 444, 555}],
                 index = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])
        self.test_gc_ser3 = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.00010_rc0.00010_n1000_dual1_rep3.tab',
                 1e-04, 1e-04, 1000, 1, 3, 'seq_800', {1, 1680}],
                 index = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])
        
        self.test_gc = pd.DataFrame(columns = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])
        self.test_gc.loc[0] = self.test_gc_ser1
        self.test_gc.loc[1] = self.test_gc_ser2
        self.test_gc.loc[2] = self.test_gc_ser3
     
        self.test_gc_match = pd.DataFrame(
                columns = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])
        self.test_gc_match.loc[0] = pd.Series(
                ['/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/msa_m0.0010_rc0.0010_n100_dual0.25_rep2.tab',
                 1e-03, 1e-03, 100, 0.25, 2, 'seq_11', {111, 222, 99, 88}],
                 index = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name', 'bp'])

    def test_sim_in_gc(self):
        """ Test string matches a string in series"""
        self.assertTrue(
                sim_in_gc(self.test_simrow1, self.test_gc))
    
    def test_sim_seq_in_gc(self):
        """ When simulated sequence is present in GC """
        self.assertTrue(
                sim_seq_in_gc(self.test_simrow1, self.test_gc))

        """ Simulated sequence is NOT present in GC """
        self.assertFalse(
                sim_seq_in_gc(self.test_simrow2, self.test_gc))
     
    def test_match_files_seq(self):
        """ When sim matches gc 
        
        Matching row is output """
        self.assertTrue(
                match_files_seq(self.test_simrow1, self.test_gc) \
                .equals(self.test_gc_match))
        
        """ When sim matches gc
        
        Correct type (set) is output for breakpoints """
        self.test_gc_row = match_files_seq(self.test_simrow1, self.test_gc)
        self.assertTrue(
                type(self.test_gc_row.iloc[0]['bp']) == set)

        """ When sim doesn't match gc """
        self.assertTrue(
                match_files_seq(self.test_simrow2, self.test_gc).empty)
    
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
                bp_length(self.test_set_sim), 3)
        
    def test_true_pos(self):
        self.assertEqual(
                true_pos(self.test_set_sim, self.test_set_gc),
                2)
                
    def test_false_pos(self):
        self.assertEqual(
                false_pos(self.test_set_sim, self.test_set_gc),
                3)
        
    def test_false_neg(self):
        self.assertEqual(
                false_neg(self.test_set_sim, self.test_set_gc),
                1)
    
    def test_true_neg(self):
        self.assertEqual(
                true_neg(1680, 2, 3, 1),
                1674)
        
if __name__ == '__main__':
    unittest.main()
    