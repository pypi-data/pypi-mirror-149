#!/usr/bin/env python3

"""Test of the observables database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')
sys.path.append('.')

try:
    import hepdata as hd
    import hepdata.names as hnm
except:
    raise unittest.SkipTest('Failed importing hepdata.names')

class TestNamesHelper(unittest.TestCase):

    def test_names_table(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = hnm.Particle.CHARGED
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)

        self.assertNotEqual(t,None)
        self.assertNotEqual(m,None)

        self.assertEqual(m.keywords(hd.Meta.CMENERGIES)[0]['values'],[13000])
        self.assertEqual(m.keywords(hd.Meta.REACTIONS)[0]['values'],
                         [sys + " --> " + parts])
        self.assertEqual(m.keywords(hd.Meta.OBSERVABLES)[0]['values'],
                         [obs])

        self.assertEqual(m.keywords(hd.Meta.PHRASES)[0]['values'],
                         [hnm.Phrase.PT_DEPENDENCE,
                          hnm.Phrase.CENT_DEPENDENCE])


    def test_1independent(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = hnm.Particle.CHARGED
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)
        i     = hnm.independent(t,var)

        self.assertEqual(i.name, var)
        self.assertEqual(i.units, hnm.Unit.var(var,None))

    def test_3independent(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = hnm.Particle.CHARGED
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)
        il    = hnm.independent(t,[var]*3)

        for i in il: 
            self.assertEqual(i.name, var)
            self.assertEqual(i.units, hnm.Unit.var(var,None))

    def test_1dependent(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = hnm.Particle.CHARGED
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)
        d     = hnm.dependent(t,obs,parts,dict(name='A',value='B'))

        self.assertEqual(d.name, obs)
        self.assertEqual(d.units, hnm.Unit.obs(obs,''))
        self.assertEqual(d.qualifiers('PARTICLE'),
                         [dict(name='PARTICLE',value=parts)])
        self.assertEqual(d.qualifiers('A'), [dict(name='A',value='B')])
        
    def test_3dependent(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = hnm.Particle.CHARGED
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)
        dl     = hnm.dependent(t,[obs]*3,parts,dict(name='A',value='B'))

        for d in dl:
            self.assertEqual(d.name, obs)
            self.assertEqual(d.units, hnm.Unit.obs(obs,''))
            self.assertEqual(d.qualifiers('PARTICLE'),
                             [dict(name='PARTICLE',value=parts)])
            self.assertEqual(d.qualifiers('A'), [dict(name='A',value='B')])

    def test_3dependent_mix(self):
        sys   = hnm.System.PP
        sqrts = 13000
        var   = hnm.Variable.NPART
        obs   = hnm.Observable.MEANPT
        parts = [hnm.Particle.CHARGED,hnm.Particle.PI_P,hnm.Particle.PI_M]
        phrs  = []
        s     = hd.submission()
        t, m  = hnm.table(s,'A table',sys,sqrts,var,obs,parts,phrs,num=1)
        pl    = [[p] for p in parts]
        dl    = hnm.dependent(t,[obs]*3,pl,dict(name='A',value='B'))

        for d,p in zip(dl,pl):
            self.assertEqual(d.name, obs)
            self.assertEqual(d.units, hnm.Unit.obs(obs,''))
            self.assertEqual(d.qualifiers('PARTICLE'),
                             [dict(name='PARTICLE',value=p[0])])
            self.assertEqual(d.qualifiers('A'), [dict(name='A',value='B')])

    def test_named_columns(self):
        sys        = hnm.System.PP
        sqrts      = 13000
        var        = [hnm.Variable.NPART,hnm.Variable.CENTRALITY]
        obs        = [hnm.Observable.MEANPT,hnm.Observable.RAA]
        parts      = [[hnm.Particle.HADRON_P,hnm.Particle.HADRON_M]]
        phrs       = []
        s          = hd.submission()
        t, m, i, d = hnm.columns(s,None,sys,sqrts,var,obs,parts,phrs,num=1)
        
        # print(m._d[hd.Meta.DESCRIPTION])
        for ii,v in zip(i,var):
            self.assertEqual(ii.name, v)
            self.assertEqual(ii.units, hnm.Unit.var(v))

        for dd,o in zip(d,obs):
            self.assertEqual(dd.name, o)
            self.assertEqual(dd.units, hnm.Unit.obs(o))
            self.assertEqual(dd.qualifiers('PARTICLE'),
                             [dict(name='PARTICLE',value=' '.join(parts[0]))])
            
        
        
            
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
