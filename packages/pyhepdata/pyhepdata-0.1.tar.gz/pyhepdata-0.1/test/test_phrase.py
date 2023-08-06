#!/usr/bin/env python3

"""Test of the phrases database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestPhrase(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.Phrase.CHARGE_EXCHANGE,	'Charge Exchange')
        self.assertEqual(hn.Phrase.CHARGED_CURRENT,	'Charged Current')
        self.assertEqual(hn.Phrase.CHARM_PRODUCTION,	'Charm production')
        self.assertEqual(hn.Phrase.XSEC,	        'Cross Section')
        self.assertEqual(hn.Phrase.DECAY,	        'Decay')
        

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
