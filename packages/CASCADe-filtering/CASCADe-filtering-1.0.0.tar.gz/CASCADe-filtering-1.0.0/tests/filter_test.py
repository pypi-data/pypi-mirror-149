#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np

from cascade_filtering.stencil import filter_image_cube_ufunc as filter_image_cube
from cascade_filtering.filtering import prepare_data_for_filtering
from cascade_filtering.filtering import DirectionalFilter

class TestFilter(unittest.TestCase):
    def setUp(self):
        # test data set, mask follows numpy masked data convention
        self.TEST_IMAGE_CUBE = np.ones((50, 128, 128), dtype=np.float64)
        self.TEST_IMAGE_ERR = np.ones((50, 128, 128), dtype=np.float64)*0.01
        self.TEST_IMAGE_MASK = np.zeros_like(self.TEST_IMAGE_CUBE, dtype=bool)
        self.TEST_IMAGE_MASK_BLANK = \
            np.zeros_like(self.TEST_IMAGE_CUBE, dtype=bool)

        # region of interest. Defined similar as numpy mask: if True do not use
        self.ROI = np.ones((128, 128), dtype=bool)
        self.ROI[20:100, 70:98] = False

        # random cosmics
        N = 80
        np.random.seed(10)
        # array of all indices
        random_indicesy = np.arange(0, self.TEST_IMAGE_CUBE.shape[1])  
        random_indicesx = np.arange(0, self.TEST_IMAGE_CUBE.shape[2]) 
        # shuffle the array
        np.random.shuffle(random_indicesx)                             
        np.random.shuffle(random_indicesy) 
        self.TEST_IMAGE_CUBE[:, random_indicesy[:N+1],
                             random_indicesx[:N+1]] = 100.0
        self.TEST_IMAGE_MASK[:, random_indicesy[:N+1],
                             random_indicesx[:N+1]] = True

        # test filter kernels
        self.FILTER_KERNEL_STACK = np.ones((20, 9, 9))
        self.FILTER_KERNEL_STACK_3D = np.ones((20, 9, 9, 9))

    def tearDown(self):
        del self.TEST_IMAGE_CUBE
        del self.TEST_IMAGE_ERR
        del self.TEST_IMAGE_MASK
        del self.FILTER_KERNEL_STACK
        del self.FILTER_KERNEL_STACK_3D
        
        del self.TEST_IMAGE_MASK_BLANK
        del self.ROI

    def test_basic_filter_one(self):
        # Test 1
        # zero pad data and create integer mask with bad pixels as 0
        # create tuple indici to select the various data
        (processed_test_image_cube, processed_test_image_mask,
         processed_test_image_error,
         processed_sub_image_index, valid_pp_data_index, valid_data_index) = \
            prepare_data_for_filtering(
                self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK, self.TEST_IMAGE_ERR,
                self.FILTER_KERNEL_STACK.shape)

        assert(processed_test_image_cube.shape[1] ==
               self.TEST_IMAGE_CUBE.shape[1]+self.FILTER_KERNEL_STACK.shape[1]-1)
        assert(np.all(self.TEST_IMAGE_CUBE[processed_sub_image_index] ==
               processed_test_image_cube[valid_pp_data_index]))
        assert(np.all(self.TEST_IMAGE_MASK[processed_sub_image_index] ==
                      ~processed_test_image_mask[valid_pp_data_index].astype(bool)))

    def test_basic_filter_two(self):
        # test 2
        (processed_test_image_cube, processed_test_image_mask,
         processed_test_image_error,
         processed_sub_image_index, valid_pp_data_index, valid_data_index) = \
            prepare_data_for_filtering(
                self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK, self.TEST_IMAGE_ERR,
                self.FILTER_KERNEL_STACK.shape)        

        filtered_cube = filter_image_cube(processed_test_image_cube,
                                          processed_test_image_mask,
                                          self.FILTER_KERNEL_STACK)

        assert(filtered_cube[valid_data_index].shape ==
               (self.FILTER_KERNEL_STACK.shape[0],) +
               processed_test_image_cube[valid_pp_data_index].shape)
        assert(np.allclose(filtered_cube[valid_data_index], 1.0))
    
    def test_basic_filter_three(self):
        # test 3, same as test 2 but with ROI applied
        (processed_test_image_cube, processed_test_image_mask,
         processed_test_image_error,
         processed_sub_image_index, valid_pp_data_index, valid_data_index) = \
            prepare_data_for_filtering(
                self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK, self.TEST_IMAGE_ERR,
                self.FILTER_KERNEL_STACK.shape, ROI=self.ROI)

        filtered_cube = filter_image_cube(processed_test_image_cube,
                                          processed_test_image_mask,
                                          self.FILTER_KERNEL_STACK)

        assert(filtered_cube[valid_data_index].shape ==
               (self.FILTER_KERNEL_STACK.shape[0],) +
               processed_test_image_cube[valid_pp_data_index].shape)
        assert(processed_test_image_mask[valid_pp_data_index][0,...].size == 
               np.sum(~self.ROI))
        assert(np.allclose(filtered_cube[valid_data_index], 1.0))
                                         
    def test_basic_filter_four(self):
        # test 4
        DF = DirectionalFilter()
        DF.load_filter_kernels(self.FILTER_KERNEL_STACK)
        DF.run_filter(self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK,
                      self.TEST_IMAGE_ERR, ROI=self.ROI)

        assert(
            DF.optimal_filtered_image_cube[DF.pp_data_cube_valid_index].shape ==
            self.TEST_IMAGE_CUBE[DF.pp_roi_image_cube_index].shape
        )

        #number of bad pixels left should be below treshold
        assert (DF.number_of_flagged_pixels <= DF.acceptance_limit)
        
        #should have found all bad pixels
        assert(np.allclose(
            ~DF.cumulative_image_cube_mask[DF.pp_data_cube_valid_index].astype(bool),
            self.TEST_IMAGE_MASK[DF.pp_roi_image_cube_index]
            )
        )

        #filtered images should be all 1
        assert(np.allclose(
            DF.filtered_image_cube[DF.filtered_data_valid_index], 1.0
            )
        )

        # should be cleaned
        assert(np.allclose(DF.pp_image_cube_mask[DF.pp_data_cube_valid_index], 1))
        assert(np.allclose(DF.pp_image_cube[DF.pp_data_cube_valid_index], 1.0))
        
    def test_basic_filter_five(self):
        # test 5
        DF = DirectionalFilter()
        DF.load_filter_kernels(self.FILTER_KERNEL_STACK)
        DF.run_filter(self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK_BLANK,
                      self.TEST_IMAGE_ERR, ROI=self.ROI)

        assert(DF.optimal_filtered_image_cube[DF.pp_data_cube_valid_index].shape ==
               self.TEST_IMAGE_CUBE[DF.pp_roi_image_cube_index].shape)

        #number of bad pixels left should be below treshold
        assert (DF.number_of_flagged_pixels <= DF.acceptance_limit)
        
        #should have found all bad pixels
        assert(np.allclose(
            ~DF.cumulative_image_cube_mask[DF.pp_data_cube_valid_index].astype(bool),
            self.TEST_IMAGE_MASK[DF.pp_roi_image_cube_index]
            )
        )

        #filtered images should be all 1
        assert(np.allclose(DF.filtered_image_cube[DF.filtered_data_valid_index], 1.0))

        # should be cleaned
        assert(np.allclose(DF.pp_image_cube_mask[DF.pp_data_cube_valid_index], 1))
        assert(np.allclose(DF.pp_image_cube[DF.pp_data_cube_valid_index], 1.0))

    def test_basic_filter_six(self):
        # test 6 using 3d kernel
        DF = DirectionalFilter()
        DF.load_filter_kernels(self.FILTER_KERNEL_STACK_3D)
        DF.run_filter(self.TEST_IMAGE_CUBE, self.TEST_IMAGE_MASK_BLANK,
                      self.TEST_IMAGE_ERR, ROI=self.ROI)

        assert(DF.optimal_filtered_image_cube[DF.pp_data_cube_valid_index].shape ==
               self.TEST_IMAGE_CUBE[DF.pp_roi_image_cube_index].shape)

        #number of bad pixels left should be below treshold
        assert (DF.number_of_flagged_pixels <= DF.acceptance_limit)
        
        #should have found all bad pixels
        assert(np.allclose(
            ~DF.cumulative_image_cube_mask[DF.pp_data_cube_valid_index].astype(bool),
            self.TEST_IMAGE_MASK[DF.pp_roi_image_cube_index]
            )
        )

        #filtered images should be all 1
        assert(np.allclose(DF.filtered_image_cube[DF.filtered_data_valid_index], 1.0))

        # should be cleaned
        assert(np.allclose(DF.pp_image_cube_mask[DF.pp_data_cube_valid_index], 1))
        assert(np.allclose(DF.pp_image_cube[DF.pp_data_cube_valid_index], 1.0))

if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFilter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)