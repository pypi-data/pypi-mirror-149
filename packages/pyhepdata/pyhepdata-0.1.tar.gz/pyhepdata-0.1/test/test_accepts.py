#!/usr/bin/env python3 
"""Test case for accepts decorator

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from hepdata.accepts import accepts

class A:
    @accepts(x=int)
    def test_int(self,x):
        return x

    @accepts(x=float)
    def test_float(self,x):
        return x

    @accepts(x=(float,str))
    def test_float_str(self,x):
        return x

    @accepts(x=(float,list))
    def test_float_list(self,x):
        return x

    @property
    def prop(self):
        return 42
    
    @prop.setter
    @accepts(x=int)
    def prop(self,x):
        pass
    


class TestAccepts(unittest.TestCase):

    def test_int(self):
        a = A()
        self.assertEqual(a.test_int(10),10)

    def test_float(self):
        a = A()
        self.assertEqual(a.test_float(3.14),3.14)
        self.assertEqual(a.test_float('3.14'),3.14)

    def test_float_str(self):
        a = A()
        self.assertEqual(a.test_float_str(3.14),3.14)
        self.assertEqual(a.test_float_str("3.14"),"3.14")
        self.assertEqual(a.test_float_str("foo"),"foo")

    def test_float_list(self):
        a = A()
        self.assertEqual(a.test_float_list(3.14),3.14)
        self.assertEqual(a.test_float_list([3.14]),[3.14])

    def test_not_int(self):

        with self.assertRaises(TypeError):
            a = A()
            a.test_int(complex(1,3))

    def test_not_float(self):

        with self.assertRaises(TypeError):
            a = A()
            a.test_float("fubar")

    def test_none(self):

        a = A()
        with self.assertRaises(TypeError):
            a.test_int(None)

    def test_property(self):
        a = A()

        self.assertEqual(a.prop, 42)

        a.prop = 3

        with self.assertRaises(TypeError):
            a.prop = "foo"
    

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
