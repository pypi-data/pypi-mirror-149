#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from cascade_filtering.kernel import define_covariance_matrix
from cascade_filtering.kernel import define_anisotropic_gaussian_kernel
from cascade_filtering.kernel import create_nagano_matsuyama_kernels
from cascade_filtering.kernel import create_kuwahara_kernels
from cascade_filtering.kernel import create_anisotropic_curved_kernels
from cascade_filtering.kernel import FilterKernel
from cascade_filtering.kernel import create_sift_kernels

class TestKernel(unittest.TestCase):
    def setUp(self):
        self.test_thetas1 = [0.0, 90.0, [0.0]]
        self.test_thetas2 = [[0.0, 0.0, 90.0]]
        self.test_sigmas1 = [1.0, [1.0], [1.0, 1.0], [1.0, 1.0, 1.0]]
        self.test_sigmas2 = [[1.0, 1.0, 1.0]]
        self.test_shapes1 = [(2,2), (2,2), (2,2), (3,3)]
        self.test_shapes2 = [(3,3)]
        self.test_thetas4 = [0.0, 90.0]
        self.cov_matrix_test4 = [np.array([[1.0, 0.0], [0.0, 9.0]]),
                                 np.array([[9.0, 0.0], [0.0, 1.0]])]

    def tearDown(self):
        del self.test_thetas1
        del self.test_thetas2
        del self.test_sigmas1
        del self.test_shapes1
        del self.test_sigmas2
        del self.test_shapes2 
        del self.test_thetas4 
        del self.cov_matrix_test4 

    def test_one(self):
        for theta in self.test_thetas1:
            for shape, sigma in zip(self.test_shapes1, self.test_sigmas1):
                cov_matrix = define_covariance_matrix(sigma=sigma, theta=theta,
                                                      degrees=True)
                assert(cov_matrix.shape == shape)

    def test_two(self):
        for theta in self.test_thetas2:
            for shape, sigma in zip(self.test_shapes2, self.test_sigmas2):
                cov_matrix = define_covariance_matrix(sigma=sigma, theta=theta,
                                                      degrees=True)
                assert(cov_matrix.shape == shape)

    def test_three(self):
         with self.assertRaises(Exception):
             self.assertRaises(ValueError, define_covariance_matrix, self,
                               sigma=1.0, max_angle=[0.0, 0.0, 0.0]) 

    def test_four(self):
        for value, theta in zip(self.cov_matrix_test4, self.test_thetas4):
            cov_matrix = define_covariance_matrix(sigma=[1.0, 3.0], theta=theta,
                                                  degrees=True)
            assert(np.allclose(cov_matrix, value))

    def test_five(self):
        kernel = define_anisotropic_gaussian_kernel((9, 9, 9),
                                                    sigma=[1.0, 3.0, 0.2],
                                                    theta=-15.0, degrees=True)
        assert(kernel.shape == (9,9,9))
        assert(np.allclose(np.sum(kernel), 1.0))
        
        kernel = define_anisotropic_gaussian_kernel((9, 9), sigma=[3.0, 0.2],
                                                    theta=-15.0, degrees=True)
        assert(kernel.shape == (9,9))
        assert(np.allclose(np.sum(kernel), 1.0))

    def test_six(self):
        kernel_stack = create_nagano_matsuyama_kernels(7)
        assert(kernel_stack.ndim == 3)
        assert(kernel_stack.shape == (17, 7, 7))
        assert(np.allclose(np.sum(kernel_stack[0,...]), 49.0))
        assert(np.allclose(np.sum(kernel_stack[2,...]), 9.0))

        kernel_stack = create_kuwahara_kernels(7)
        assert(kernel_stack.ndim == 3)
        assert(kernel_stack.shape == (15, 7, 7))
        assert(np.allclose(np.sum(kernel_stack[0,...]), 49.0))
        assert(np.allclose(np.sum(kernel_stack[2,...]), 9.0))        

        kernel_stack = create_anisotropic_curved_kernels(7)
        assert(kernel_stack.ndim == 3)
        assert(kernel_stack.shape == (18, 7, 7))
        assert(np.allclose(np.sum(kernel_stack[0,...],axis=0)[3], 1.0))
        
     
    def test_seven(self):
        FK = FilterKernel(configuration_file='anisotropic_gaussian_kernel.conf')
        assert(FK.kernel_stack.shape == (25+6, 9, 9, 9))
        FK = FilterKernel(configuration_file='anisotropic_gaussian_kernel_2d.conf')
        assert(FK.kernel_stack.shape == (25, 9, 9))
        FK = FilterKernel(configuration_file='banana_kernel.conf')
        assert(FK.kernel_stack.shape == (18, 9, 9))
        FK = FilterKernel(configuration_file='kuwahara_kernel.conf')
        assert(FK.kernel_stack.shape == (15, 7, 7))
        FK = FilterKernel(configuration_file='nagano_matsuyama_kernel.conf')
        assert(FK.kernel_stack.shape == (17, 7, 7))

    def test_eight(self):
        kernel, multiplier, sigma = create_sift_kernels()
        assert(kernel.shape == (11, 11,11))
        assert(np.allclose(np.sum(kernel, axis=(1,2)), 1.0))
        assert(np.allclose(sigma, 0.5))


if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKernel)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)