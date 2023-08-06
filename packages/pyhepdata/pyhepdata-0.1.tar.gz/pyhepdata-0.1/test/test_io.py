#!/usr/bin/env python3 
"""Test case for I/O and validation 

Copyright 2019 Christian Holm Christensen
"""
import math
import unittest
import io
import sys
import os
import random
from pprint import pprint 
sys.path.append('..')
sys.path.append('.')

from hepdata import Submission
from hepdata import Meta
from hepdata import Table
from hepdata.io import FileIO, ZipIO, Validator, dump, load
from examples.fill import fill
from examples.simple import make

class TestIO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fd = os.path.dirname(__file__)
        wd = os.getcwd()
        sub = fd.replace(wd,'')
        if len(sub) > 0 and sub.startswith(os.path.sep):
            sub = sub[1:]
        cls._sub = sub
        
    def _makeSubmission(self,name,same=False,newstyle=False):
        s, m, t = make(name,same,newstyle)
        fill(t)
        m.resource('dndetarap.png','Image')
        m.resource('dndyrap.png',  'Image')
        
        return s, m, t

    def _forcerm(self,filename):
        if os.path.isfile(filename):
            # print('Removing {}'.format(filename))
            os.unlink(filename)
            # os.rename(filename,filename+".old")
        
    def _cleanOld(self,name):
        self._forcerm(name+'.yaml')
        self._forcerm(name+'_tab.yaml')
        self._forcerm(name+'.zip')

    def _read_write(self,name,
                    same=False,
                    validate=False,
                    newstyle=False):
        fname = os.path.join(self._sub,name)
        self._cleanOld(fname)
        v = None
        if validate:
            v = Validator(verb=False,compat=same)
            
        s,m,t = self._makeSubmission(name,same,newstyle)
        
        rw = FileIO(v,verbose=False)
        rw.dump(s,filename=fname+'.yaml')

        s2 = rw.load(filename=fname+'.yaml')

        self.maxDiff = None
        self.assertEqual(s._d, s2._d)
        self.assertEqual(m._d, s2._t[m.name]._d)
        self.assertEqual(t._d, s2._t[m.name]._t._d)

    def test_load_dump(self):
        name = 'ld'
        fname = os.path.join(self._sub,name)
        self._cleanOld(fname)
        s,m,t = self._makeSubmission(name,False)

        dump(s,filename=fname+'.yaml',validator=True)
        s2 = load(filename=fname+'.yaml',validator=True)
        self.assertNotEqual(s2,None)
        self.assertEqual(s._d, s2._d)
        
        t2 = load(filename=fname+'_tab.yaml',validator=True)
        self.maxDiff = None
        self.assertNotEqual(t2,None)
        self.assertEqual(t._d, t2._d)

    def test_zip(self):
        name = 'archive'
        fname = os.path.join(self._sub,name)
        self._cleanOld(fname)
        s,m,t = self._makeSubmission(name,False)

        dump(s,filename=fname+'.zip',validator=True,verbose=False)
        s2 = load(filename=fname+'.zip',validator=True,verbose=False)
        self.assertEqual(s._d, s2._d)
        self.assertEqual(m._d, s2._t[m.name]._d)
        self.assertEqual(t._d, s2._t[m.name]._t._d)
        
    def test_zip_direct(self):
        name = 'archive2'
        fname = os.path.join(self._sub,name)
        self._cleanOld(fname)
        s,m,t = self._makeSubmission(name,False)

        rw = ZipIO(Validator(),verbose=False)
        rw.dump(s,filename=fname+'.zip')
        s2 = rw.load(filename=fname+'.zip')
        self.assertEqual(s._d, s2._d)
        self.assertEqual(m._d, s2._t[m.name]._d)
        self.assertEqual(t._d, s2._t[m.name]._t._d)

    def test_tgz(self):
        name = 'archive'
        fname = os.path.join(self._sub,name)
        self._cleanOld(fname)
        s,m,t = self._makeSubmission(name,False)

        dump(s,filename=fname+'.tgz',validator=True,verbose=False)
        s2 = load(filename=fname+'.tgz',validator=True,verbose=False)
        self.assertEqual(s._d, s2._d)
        self.assertEqual(m._d, s2._t[m.name]._d)
        self.assertEqual(t._d, s2._t[m.name]._t._d)

    def test_read_write(self):
        self._read_write("rw")

    def test_read_write_same(self):
        self._read_write("rw_same",True)

    def test_validate_read_write(self):
        self._read_write("vrw",False,True)

    def test_validate_read_write_same(self):
        self._read_write("vrw_same",True,True)
        
    def test_validate_read_write_same_new(self):
        self._read_write("vrw_same_new",False,True,True)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
