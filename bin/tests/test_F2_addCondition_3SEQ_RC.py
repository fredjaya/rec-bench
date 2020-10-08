#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:02:43 2020

@author: Fred Jaya
"""

import unittest
import pandas as pd

class testFunctions(unittest.TestCase):
    
    def setUp(self):
        
        """ From msa_m0.0010_rc0.00010_n100_dual1_rep2.fasta.3s.rec """
        self.test_predicted_rec = pd.DataFrame(
                columns = ['P_ACCNUM', 'Q_ACCNUM', 'C_ACCNUM', 'm', 'n', 'k',
                           'p', 'HS?', 'log(p)', 'DS(p)', 'DS(p)', 
                           'min_rec_length', 'breakpoints'])
    
        self.test_predicted_rec.loc[1] = ['seq_82', 'seq_52', 'seq_68', '8', 
                                          '50', '50', '0.000000004695', '0', 
                                          '-8.3283', '0.00455', '4.545052e-03',
                                          '757', ' 0-0 & 757-794']
        self.test_predicted_rec.loc[2] = ['seq_82', 'seq_32', 'seq_2', '2', 
                                          '53', '53', '0.00000000481', '0', 
                                          '-6.3863', '0.00235', '3.589052e-03',
                                          '757', ' 0-0 & 650-695']
    
        self.test_sim_row1 = pd.Series(
                {'params': 'msa_m0.00010_rc0.00010_n100_dual0.05_rep3.fasta.3s.rec',
                 'seq': 'seq_23', 
                 'breakpoints': float('nan')})

        self.test_sim_row2 = pd.Series(
                {'params': 'msa_m0.0010_rc0.000010_n1000_dual1_rep2.fasta.3s.rec',
                 'seq': 'seq_68', 
                 'breakpoints': float('nan')})
    
        self.test_match = pd.DataFrame(
                columns = ['P_ACCNUM', 'Q_ACCNUM', 'C_ACCNUM', 'm', 'n', 'k',
                           'p', 'HS?', 'log(p)', 'DS(p)', 'DS(p)', 
                           'min_rec_length', 'breakpoints'])
        self.test_match.loc[1] = ['seq_82', 'seq_52', 'seq_68', '8', '50', 
                                  '50', '0.000000004695', '0', '-8.3283', 
                                  '0.00455', '4.545052e-03', '757', 
                                  ' 0-0 & 757-794']
        
    def test_match_seq(self):
        """ Non-matching seqs returns empty dataframe """
        self.assertTrue(
                match_seq(self.test_sim_row1, self.test_predicted_rec).empty)
        
        """ Matching seqs returns row of seq """
        self.assertTrue(
                match_seq(self.test_sim_row2, self.test_predicted_rec).equals(
                        self.test_match))
        
if __name__ == '__main__':
    unittest.main()

x = match_seq(test_sim_row2, test_predicted_rec)