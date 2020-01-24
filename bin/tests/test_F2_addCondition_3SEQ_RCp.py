#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 08:26:23 2020

@author: Fred Jaya

Tests for F2_addCondition_3SEQ_RCp.py
"""

import unittest
import pandas as pd

class testFunctions(unittest.TestCase):

    def readRecFile_testMod(x):
        recFile = pd.DataFrame([line.strip().split('\t') 
                    for line in open(x, 'r')])
        newHeader = recFile.iloc[0]
        recFile = recFile[1:]
        recFile.columns = newHeader
        return(recFile)
    
    def setUp(self):
        self.test_simSeq_unmatch = pd.Series(
                {'params': 'msa_m0.0010_rc0.000010_n100_dual0.1_rep1.fasta.3s.rec',
                    'seq': 'seq_9999999',
            'breakpoints': float('NaN')})
    
        self.test_simSeq_matchMultiBP = pd.Series(
                {'params': 'msa_m0.010_rc0.010_n100_dual1_rep2.fasta.3s.rec',
                    'seq': 'seq_3',	
            'breakpoints': 891})
    
        self.test_predictedRec_Norm    = readRecFile_testMod("/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/B2_3seq/RCp/msa_m0.0010_rc0.000010_n100_dual0.1_rep1.fasta.3s.rec")
        self.test_predictedRec_MultiBP = readRecFile_testMod("/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/B2_3seq/RCp/msa_m0.010_rc0.010_n100_dual1_rep2.fasta.3s.rec")
        self.test_predictedRec_DupSeq  = self.test_predictedRec_MultiBP.append(
                self.test_predictedRec_MultiBP)
    
    def test_getPredictedSeqs(self):
        ''' 
        Single row 
        '''
        self.assertEqual(getPredictedSeqs(self.test_simSeq_unmatch,
                                          self.test_predictedRec_Norm), ['seq_45'],
                         'Predicted sequences don\'t match')
    
        ''' 
        Multiple rows with simulated breakpoints appended 
        '''
        self.assertEqual(getPredictedSeqs(self.test_simSeq_unmatch,
                                          self.test_predictedRec_MultiBP), 
                         ['seq_3', 'seq_8', 'seq_18', 'seq_41', 'seq_45', 
                          'seq_51', 'seq_70'],
                          'Predicted sequences don\'t match')
        
        ''' 
        Duplicate sequence 
        '''
        self.assertEqual(getPredictedSeqs(self.test_simSeq_unmatch, 
                                          self.test_predictedRec_DupSeq), 
                                            -1)
        
    def test_getPredictedBPs(self):
        ''' 
        Data with multiple breakpoints predicted, when one sequence matches only one 
        pair of bps 
        '''
        self.assertEqual(getPredictedBPs(self.test_simSeq_matchMultiBP,
                                         self.test_predictedRec_MultiBP),
                                        [44, 45, 46, 763, 764, 765])
        
        ''' 
        Data with multiple breakpoints predicted, and sequence matches more
        than one breakpoint pairs
        '''
        
        
        ''' 
        When simSeq is not present in predictedRec
        '''
        self.assertEqual(getPredictedBPs(self.test_simSeq_unmatch, 
                                         self.test_predictedRec_MultiBP),
                                         -1)

if __name__ == '__main__':
    unittest.main()