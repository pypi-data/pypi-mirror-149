#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from cascade_filtering.stencil import stencil_kernel9 as stencil_kernel
from cascade_filtering.stencil import stencil_kernel9_3d as stencil_kernel_3d
from cascade_filtering.stencil import filter_image_cube_ufunc as filter_image_cube
from cascade_filtering.stencil import stencil_local_maximum

class TestStencil(unittest.TestCase):
    def setUp(self):
        # test data set
        # Note that the mask is integer and one for "good" pixels
        self.TEST_IMAGE_CUBE = np.ones((50, 128, 128), dtype=np.float64)
        self.TEST_IMAGE_MASK = np.ones_like(self.TEST_IMAGE_CUBE, dtype=np.int8)
        self.TEST_ZERO_IMAGE_MASK = np.ones_like(self.TEST_IMAGE_CUBE, dtype=np.int8)

        # random cosmics
        N = 40
        random_indicest = np.arange(0, self.TEST_IMAGE_CUBE.shape[0])  
        random_indicesy = np.arange(0, self.TEST_IMAGE_CUBE.shape[1])    # array of all indices
        random_indicesx = np.arange(0, self.TEST_IMAGE_CUBE.shape[2])
        np.random.shuffle(random_indicest) 
        np.random.shuffle(random_indicesx)                          # shuffle the array
        np.random.shuffle(random_indicesy) 
        self.TEST_IMAGE_CUBE[random_indicest[:N+1], random_indicesy[:N+1], random_indicesx[:N+1]] = 100.0
        self.TEST_IMAGE_MASK[random_indicest[:N+1], random_indicesy[:N+1], random_indicesx[:N+1]] = 0

        # test filter kernels
        self.DIRECTIONAL_FILTERS = np.ones((20, 9, 9))
        self.DIRECTIONAL_FILTERS_3D = np.ones((20, 9, 9, 9))

    def tearDown(self):
        del self.TEST_IMAGE_CUBE
        del self.TEST_IMAGE_MASK
        del self.TEST_ZERO_IMAGE_MASK
        del self.DIRECTIONAL_FILTERS
        del self.DIRECTIONAL_FILTERS_3D

    def test_basic_stencil_one(self):
        filtered_image = stencil_kernel(self.TEST_IMAGE_CUBE[0,...], 
                                        self.TEST_IMAGE_MASK[0, ...],
                                        self.DIRECTIONAL_FILTERS[0, ...])

        assert(filtered_image.ndim == 2)
        assert(filtered_image.shape == (128, 128))
        assert(not np.allclose(self.TEST_IMAGE_CUBE[0, ...], 1.0))
        assert(np.allclose(filtered_image[4:-4, 4:-4], 1.0))

    def test_basic_stencil_two(self):
        filtered_image_cube = stencil_kernel_3d(self.TEST_IMAGE_CUBE, 
                                                self.TEST_IMAGE_MASK,
                                                self.DIRECTIONAL_FILTERS_3D[0, ...])

        assert(filtered_image_cube.ndim == 3)
        assert(filtered_image_cube.shape == (50, 128, 128))
        assert(not np.allclose(self.TEST_IMAGE_CUBE, 1.0))
        assert(np.allclose(filtered_image_cube[4:-4, 4:-4, 4:-4], 1.0))       
    
    def test_basic_filter_cube(self):
        filtered_cube = filter_image_cube(self.TEST_IMAGE_CUBE,
                                          self.TEST_IMAGE_MASK,
                                          self.DIRECTIONAL_FILTERS)
 
        assert(filtered_cube.ndim == 4)
        assert(filtered_cube.shape == (20, 50, 128, 128))
        assert(not np.allclose(self.TEST_IMAGE_CUBE, 1.0))
        assert(np.allclose(filtered_cube[:, :, 4:-4, 4:-4], 1.0))

    def test_basic_filter_cube_two(self):
        filtered_cube = filter_image_cube(self.TEST_IMAGE_CUBE,
                                          self.TEST_IMAGE_MASK,
                                          self.DIRECTIONAL_FILTERS_3D)
 
        assert(filtered_cube.ndim == 4)
        assert(filtered_cube.shape == (20, 50, 128, 128))
        assert(not np.allclose(self.TEST_IMAGE_CUBE, 1.0))
        assert(np.allclose(filtered_cube[:, 4:-4, 4:-4, 4:-4], 1.0))

    def test_sift_stencil(self):
        filtered_image_cube = stencil_local_maximum(self.TEST_IMAGE_CUBE,
                                                    self.TEST_IMAGE_MASK)
        assert(np.allclose(filtered_image_cube, 0))
        filtered_image_cube = stencil_local_maximum(self.TEST_IMAGE_CUBE,
                                                    self.TEST_ZERO_IMAGE_MASK)
        assert(np.sum(filtered_image_cube) ==
               np.sum(~self.TEST_IMAGE_MASK.astype(bool)[1:-1, 1:-1, 1:-1]))
    

if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStencil)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)