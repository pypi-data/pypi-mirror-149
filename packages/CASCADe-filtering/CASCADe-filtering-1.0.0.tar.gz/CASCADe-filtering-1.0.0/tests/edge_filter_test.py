#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np

from cascade_filtering.filtering import EdgeFilter

class TestEdgeFilter(unittest.TestCase):
    def setUp(self):
        # test data set, mask follows numpy masked data convention
        self.TEST_IMAGE_CUBE = np.ones((50, 128, 128), dtype=np.float64)
        self.TEST_IMAGE_ERR = np.ones((50, 128, 128), dtype=np.float64)*0.01
        self.TEST_IMAGE_MASK = np.zeros_like(self.TEST_IMAGE_CUBE, dtype=bool)

        # region of interest. Defined similar as numpy mask: if True do not use
        self.ROI = np.ones((128, 128), dtype=bool)
        self.ROI[20:100, 70:100] = False

        #source
        self.TEST_IMAGE_CUBE[:, 30:90, 85] = 100.0
        self.TEST_IMAGE_CUBE2 = self.TEST_IMAGE_CUBE.copy()
        self.TEST_IMAGE_CUBE2[:, 20:80, 35] = 90.0

    def tearDown(self):
        del self.TEST_IMAGE_CUBE
        del self.TEST_IMAGE_CUBE2
        del self.TEST_IMAGE_ERR
        del self.TEST_IMAGE_MASK
        del self.ROI

    def test_basic_filter_one(self):
        # test 1
        EF = EdgeFilter()
        EF.run_filter(self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK)
        EF.derive_source_location()
        assert(len(EF.source_location.source_traces) == 1)
        assert(EF.source_location.number_of_sources == 1)
        assert(np.allclose(EF.source_location.source_traces[0][0][0], 85))
        angles = EF.filtering_results.trace_angle[EF.data.pp_data_cube_valid_index][5, 32:87, 85]
        assert(np.allclose(angles, 0.5*np.pi, atol=0.1))

    def test_basic_filter_two(self):
        # test 2
        EF = EdgeFilter()
        EF.run_filter(self.TEST_IMAGE_CUBE2, self.TEST_IMAGE_MASK)
        EF.derive_source_location()
        assert(len(EF.source_location.source_traces) == 2)
        assert(EF.source_location.roi.shape[0] == 2)
        assert(EF.source_location.number_of_sources == 2)
        assert(np.allclose(EF.source_location.source_traces[0][0][0], 35))
        assert(np.allclose(EF.source_location.source_traces[1][0][0], 85))


if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEdgeFilter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)