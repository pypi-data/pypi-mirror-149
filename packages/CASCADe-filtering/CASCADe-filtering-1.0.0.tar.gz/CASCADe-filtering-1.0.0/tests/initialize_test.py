#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from cascade_filtering.initialize import check_cascade_version


class TestKernel(unittest.TestCase):
    def setUp(self):
        self.test_version = 'main'
        self.test_version_not_excisting = 'bla'
        
    def tearDown(self):
        del self.test_version
        del self.test_version_not_excisting

    def test_one(self):
       use_version = check_cascade_version(self.test_version)
       assert(use_version == 'main')
       use_version = check_cascade_version(self.test_version_not_excisting)
       assert(use_version == 'main')


if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKernel)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)