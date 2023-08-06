#!/usr/bin/env python3

"""Test of the particles database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestParticle(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.Particle.GAMMA,	'GAMMA')
        self.assertEqual(hn.Particle.HIGGS,	'HIGGS')
        self.assertEqual(hn.Particle.F0_500,	'F0(500)')
        self.assertEqual(hn.Particle.D_STAR_S0_2317_P,'D*/S0(2317)+')

    def test_pretty(self):
        self.assertEqual(hn.Particle.pretty(hn.Particle.GAMMA),
                         r'$\mathrm{\gamma}$')
        self.assertEqual(hn.Particle.pretty(hn.Particle.HIGGS),
                         r'$\mathrm{H}$')
        self.assertEqual(hn.Particle.pretty(hn.Particle.F0_500),
                         r'$\mathrm{F}_{0}(500)$')
        self.assertEqual(hn.Particle.pretty(hn.Particle.D_STAR_S0_2317_P),
                         r'$\mathrm{D}^{*}/S_{0}(2317)^{+}$')

    def test_register(self):
        hn.Particle.register('FOO','BAR',r'\mathrm{Foo}')
        self.assertEqual(hn.Particle.FOO,	'BAR')
        self.assertEqual(hn.Particle.pretty(hn.Particle.FOO),
                         r'$\mathrm{Foo}$')

    def test_missing(self):
        with self.assertRaises(NameError):
            print(Particle.FUBAR)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
