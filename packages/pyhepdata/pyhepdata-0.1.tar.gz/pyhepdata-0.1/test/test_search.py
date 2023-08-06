#!/usr/bin/env python3 
"""Test case for Search

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from pprint import pprint 
from hepdata.search import Search

class TestSearch(unittest.TestCase):

    @unittest.skip('Takes too long')
    def test_plb650_219(self):
        s = Search()
        data = s.query('find j Phys.Lett.,B650,219')[0]
        del data['abstract']
        exp = {'accelerator_experiment':{'experiment':'BNL-RHIC-BRAHMS'},
               'doi': '10.1016/j.physletb.2007.05.017',
               'license': {'license': 'CC-BY-3.0',
                           'url':'http://creativecommons.org/licenses/by/3.0/'},
               'prepublication': {'date': '2006-10'},
               'primary_report_number': 'nucl-ex/0610021',
               'publication_info': {'pagination': '219-223',
                                    'title': 'Phys.Lett.',
                                    'volume': 'B650',
                                    'year': '2007'},
               'recid': 729167,
               'system_number': {'value': 'SPIRES-6939295'}}
        self.assertEqual(data,exp)
        # pprint(data)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
