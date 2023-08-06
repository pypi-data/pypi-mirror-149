#!/usr/bin/env python3 
"""Test case for Singleton

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from pprint import pprint 
from hepdata.singleton import Singleton

class A(metaclass=Singleton):
    def __init__(self):
        pass

class TestSingleton(unittest.TestCase):

    def test_there_can_be_only_one(self):
        a = A()
        b = A()

        self.assertEqual(id(a),id(b))

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
