#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:59:44 2022

@author: bouwman
"""
import os
import numpy as np
from typing import Tuple
import copy
import warnings
from scipy import ndimage
import pathlib
import configparser
import ast
from types import SimpleNamespace

from cascade_filtering.stencil import filter_image_cube_ufunc as filter_image_cube
from cascade_filtering.kernel import create_sobel_kernels
from cascade_filtering.kernel import create_schar_kernels
from cascade_filtering.kernel import create_gaussian_kernel
from cascade_filtering.stencil import filter_image_cube_edge_detection
from cascade_filtering.stencil import non_max_suppression
from cascade_filtering.stencil import filter_hysteresis
from cascade_filtering import __path__

__all__ = ['prepare_data_for_filtering', 'DirectionalFilter', 'EdgeFilter']

CONFIG_PATH = pathlib.Path(os.path.dirname(__path__[0])) / 'configuration_files/'


def prepare_data_for_filtering(
   image_cube: np.ndarray, mask_cube: np.ndarray = None,
   uncertainty_cube: np.ndarray = None, kernel_stack_shape: tuple = (2, 3, 3),
   ROI: np.ndarray=None, pad_mode: str = 'constant') -> \
        Tuple[np.ndarray, np.ndarray, np.ndarray, tuple, tuple, tuple]:
    """
    Preprocess input data for filtering.

    Parameters
    ----------
    image_cube : np.ndarray
        Spectral image cube.
    mask_cube : 'np.ndarray' of 'bool'
        Pixel mask indicating valid data
    uncertainty_cube : np.array
        Uncertainty estimate per pixel
    kernel_stack_shape : tuple
        Shape of the convolution kernel
    ROI : TYPE, optional
        Region of interest. The default is None.

    Returns
    -------
    adjusted_image_cube : TYPE
        zero padded spectral image cube
    adjusted_mask_cube : np.array of np.int8
        zero padded pixel mask
    adjusted_uncertainty_cube : np.array
        zero padded uncertainty cube
    sub_image_idex : TYPE
        DESCRIPTION.
    valid_pp_data_index : TYPE
        DESCRIPTION.
    valid_filtered_data_index : TYPE
        DESCRIPTION.

    """
    if ROI is None:
        adjusted_image_cube = image_cube
        adjusted_mask_cube = mask_cube
        adjusted_uncertainty_cube = uncertainty_cube
        sub_image_idex = np.ix_(np.ones((image_cube.shape[0]), dtype=bool),
                                np.ones((image_cube.shape[1]), dtype=bool),
                                np.ones((image_cube.shape[2]), dtype=bool))
    else:
       sub_image_idex = \
           np.ix_(np.arange(image_cube.shape[0]), (~ROI).any(1), (~ROI).any(0))
       adjusted_image_cube = image_cube[sub_image_idex]
       if uncertainty_cube is not None:
           adjusted_uncertainty_cube = uncertainty_cube[sub_image_idex]
       else:
           adjusted_uncertainty_cube = uncertainty_cube
       if mask_cube is not None:
           adjusted_mask_cube = mask_cube[sub_image_idex]
       else:
           adjusted_mask_cube = mask_cube

    if len(kernel_stack_shape) == 3:
         KHWz = 0
         KHWy = kernel_stack_shape[1]//2
         KHWx = kernel_stack_shape[2]//2
    elif len(kernel_stack_shape) == 4:
        KHWz = kernel_stack_shape[1]//2
        KHWy = kernel_stack_shape[2]//2
        KHWx = kernel_stack_shape[3]//2
    else:
        raise ValueError("Kernel shape not valid")

    adjusted_image_cube = \
        np.pad(adjusted_image_cube, ((KHWz, KHWz),(KHWy, KHWy), (KHWx, KHWx)),
               pad_mode)
    if adjusted_uncertainty_cube is not None:
        adjusted_uncertainty_cube = \
            np.pad(adjusted_uncertainty_cube, ((KHWz, KHWz),(KHWy, KHWy), (KHWx, KHWx)),
                   pad_mode)
    if adjusted_mask_cube is not None:
        adjusted_mask_cube = \
            np.pad(adjusted_mask_cube, ((KHWz, KHWz),(KHWy, KHWy), (KHWx, KHWx)),
                   'constant', constant_values=True)
        adjusted_mask_cube = (~adjusted_mask_cube).astype(np.int8)

    adjusted_data_shape = adjusted_image_cube.shape

    valid_filtered_data_index = np.ix_(np.arange(kernel_stack_shape[0]),
                                       np.arange(KHWz, adjusted_data_shape[0]-KHWz),
                                       np.arange(KHWy, adjusted_data_shape[1]-KHWy),
                                       np.arange(KHWx, adjusted_data_shape[2]-KHWx))
    valid_pp_data_index = np.ix_(np.arange(KHWz, adjusted_data_shape[0]-KHWz),
                                 np.arange(KHWy, adjusted_data_shape[1]-KHWy),
                                 np.arange(KHWx, adjusted_data_shape[2]-KHWx))

    return (adjusted_image_cube, adjusted_mask_cube, adjusted_uncertainty_cube,
            sub_image_idex, valid_pp_data_index, valid_filtered_data_index)


class DirectionalFilter:
    """
    Directional Filter Class.

    This class contains all functionality to detect and clean cosmic hits in
    spectral image cubes using anisotropic (directional) filters. The applied
    filtering preserved the spatial profile of the dispersed light, such that a
    extraction profile can be derived for optimal extraction without broadening
    of the profile.

    The applied procedure is schemeticaly the following:
        - filter image cube using a stack of filter kernels
        - filter squared image cube
        - determine the variance for each pixel for each filter profile
        - determine which filter results in the minimum variance for each pixel
        - determine deviating pixels based on the minimum variance of the pixel
          neighbourhood
        - update the image_cube and mask
        - iterate untill converged.
    """

    def __init__(self, directional_filter_kernels=None, sigma=8.0,
                 acceptance_treshold=0.0001, max_iterations=20):
        self.filter_kernels = directional_filter_kernels
        self.sigma = sigma
        self.acceptance_treshold = \
            self.check_acceptance_treshold(acceptance_treshold)
        self.max_iterations =  self.check_max_iterations(max_iterations)

    def load_filter_kernels(self, directional_filter_kernels):
        self.filter_kernels = directional_filter_kernels
        self.check_filter_kernels()

    @staticmethod
    def check_acceptance_treshold(acceptance_treshold):
        if (acceptance_treshold < 1.0e-9) | (acceptance_treshold > 0.1):
            warnings.warn("Value acceptance_treshold not valid, setting it to 0.0001")
            acceptance_treshold = 0.0001
        return acceptance_treshold

    @staticmethod
    def check_max_iterations(max_iterations):
        if (max_iterations < 2) | (max_iterations > 1000):
            warnings.warn("Maximum iterations value not valid, setting it to 20.")
            max_iterations = 20
        return max_iterations

    def run_filter(self, image_cube, image_cube_mask, image_cube_error, ROI=None):
        """
        Run the iterative filtering.

        Parameters
        ----------
        image_cube : 'nd.array' of 'flaot'
            spectral image cube
        image_cube_mask : 'nd.array' of 'bool'
            pixel mask
        image_cube_error : 'nd.array' or 'float'
            pixel uncertainty.
        ROI : 'nd.array' of 'bool', optional
            Region of interest. The default is None.

        Returns
        -------
        None

        """
        self.check_filter_kernels()
        self.check_data(image_cube, image_cube_mask, ROI=ROI)

        # pp data is used to store filered data
        # need a copy of the original mask to store flaged pixels
        self.input_data_shape = image_cube.shape
        (self.pp_image_cube, self.pp_image_cube_mask, self.pp_image_cube_error,
         self.pp_roi_image_cube_index , self.pp_data_cube_valid_index,
         self.filtered_data_valid_index) = \
            prepare_data_for_filtering(image_cube, image_cube_mask,
                                       image_cube_error,
                                       self.filter_kernels.shape, ROI=ROI)

        self.cumulative_image_cube_mask = copy.copy(self.pp_image_cube_mask)

        self.number_of_flagged_pixels = \
            np.sum(self.pp_image_cube_mask[self.pp_data_cube_valid_index] == 0)

        #self.acceptance_limit = \
        #    np.min([int(self.acceptance_treshold * \
        #        self.pp_image_cube[self.pp_data_cube_valid_index].size),
        #            self.number_of_flagged_pixels])
        self.acceptance_limit = int(self.acceptance_treshold * \
                self.pp_image_cube[self.pp_data_cube_valid_index].size)

        iiteration = 1
        while ((self.number_of_flagged_pixels  > self.acceptance_limit) & \
                 (iiteration <= self.max_iterations)) | (iiteration == 1):
            print(f"iteration: {iiteration}, number of flagged pixel: {self.number_of_flagged_pixels}")
            # find bad pixels
            self.apply_filter()
            self.analyze_variance()
            self.sigma_clip()
            # second pass with bad pixels flagged to get better mean.
            self.apply_filter()
            self.analyze_variance()
            # clean data
            self.clean_image_cube()

            iiteration += 1
        if (iiteration > self.max_iterations) & \
                 (self.number_of_flagged_pixels < self.acceptance_limit):
             warnings.warn("Iteration not converged in "
                           "iterative_bad_pixel_flagging. {} mask values not "
                           "converged. An increase of the maximum number of "
                           "iteration steps might be advisable.".
                           format(self.number_of_flagged_pixels-self.acceptance_limit))
        print(f"Final number of still flagged pixel after iterations: {self.number_of_flagged_pixels}")
        print(f"The acceptance limit is: {self.acceptance_limit}")

    @staticmethod
    def check_data(image_cube, image_cube_mask, ROI=None):
        """
        Check data format.

        Parameters
        ----------
        image_cube : 'ndarray' of 'float'
            Input spectral data cube.
        image_cube_mask : 'ndarray' of 'bool'
            Pixel mask of the input data cube.
        ROI : 'ndarray' of 'bool', optional
            Region of interest. The default is None.

        Raises
        ------
        ValueError
            Is raised if input data format is not correct.

        Returns
        -------
        None

        """
        if (image_cube.shape != image_cube_mask.shape):
            raise ValueError("Data cube and data mask do not have the same size.")
        if (image_cube.ndim != 3):
            raise ValueError("Data not an image cube.")
        if not (ROI is None):
            if ROI.shape != image_cube.shape[1:]:
                raise ValueError("ROI and data cube not compatable")

    def check_filter_kernels(self):
        """
        Check kernel format.

        Raises
        ------
        ValueError
            Is raised if format is not correct.

        Returns
        -------
        None

        """
        if self.filter_kernels is None:
            raise ValueError("No filter kernels loaded.")
        if (not self.filter_kernels.ndim in [3, 4]):
            raise ValueError("Filter kernel steck needs to be 3d or 4d.")
        if (self.filter_kernels.shape[-2] != self.filter_kernels.shape[-1]):
            raise ValueError("Filter kernel needs to be square.")
        if self.filter_kernels.ndim == 4:
            if (self.filter_kernels.shape[-3] != self.filter_kernels.shape[-1]):
                raise ValueError("Filter kernel needs to be a cube.")
        if (self.filter_kernels.shape[-2]%2 -1):
            raise ValueError("Filter kernel width needs to be odd.")

    def apply_filter(self):
        """
        Apply filter to the data cubes.

        Returns
        -------
        None

        """
        self.filtered_image_cube = \
            filter_image_cube(self.pp_image_cube,
                              self.pp_image_cube_mask,
                              self.filter_kernels)
        self.filtered_image_cube_square = \
            filter_image_cube(self.pp_image_cube**2,
                              self.pp_image_cube_mask,
                              self.filter_kernels)

    def analyze_variance(self):
        """
        Calculate the variance and find the minimum.

        Returns
        -------
        None

        """
        variance = self.filtered_image_cube_square - self.filtered_image_cube**2

        valid_mask = np.ones_like(variance, dtype=bool)
        valid_mask[self.filtered_data_valid_index] = False
        I = np.ma.argmin(np.ma.array(variance, mask=valid_mask), axis=0)
        self.index_optimal_filter_kernel = \
             (I,) + np.ix_(*[np.arange(i) for i in variance.shape[1:]])

        self.optimal_filtered_image_cube = \
            self.filtered_image_cube[self.index_optimal_filter_kernel]
        self.optimal_filtered_variance = variance[self.index_optimal_filter_kernel]

    def clean_image_cube(self):
        """
        Clean bad pixels.

        Returns
        -------
        None

        """
        self.cumulative_image_cube_mask *= self.pp_image_cube_mask
        mask = self.pp_image_cube_mask == 0
        self.pp_image_cube[mask] = \
            self.optimal_filtered_image_cube[mask]
        self.pp_image_cube_error[mask] = \
            np.sqrt(self.optimal_filtered_variance[mask])
        mask_temp = self.pp_image_cube_mask[self.pp_data_cube_valid_index]
        mask_temp[mask[self.pp_data_cube_valid_index]] = 1
        self.pp_image_cube_mask[self.pp_data_cube_valid_index] = mask_temp


    def sigma_clip(self):
        """
        Sigma clip data.

        Returns
        -------
        None

        """
        mask = ((self.pp_image_cube-self.optimal_filtered_image_cube)**2 >
                (self.sigma * self.optimal_filtered_variance) + np.finfo(float).resolution)
        self.number_of_flagged_pixels = np.sum(mask)
        self.pp_image_cube_mask[mask] = 0

    def return_cleaned_data(self):
        """
        Returns cleaned data set.

        Returns
        -------
        cleaned_data : 'ndarray' of 'float'
            Cleaned data cube.
        cleaned_data_uncertainty : 'ndarray' of 'float'
            Uncertainty on the cleaned data cube.
        cleaned_data_mask : 'ndarray' of 'bool'
            Pixel mask of the cleaned data cube.

        """
        cleaned_data = np.zeros(self.input_data_shape)
        cleaned_data[self.pp_roi_image_cube_index] = \
            self.pp_image_cube[self.pp_data_cube_valid_index]

        cleaned_data_uncertainty = np.zeros(self.input_data_shape)
        cleaned_data_uncertainty[self.pp_roi_image_cube_index] = \
            self.pp_image_cube_error[self.pp_data_cube_valid_index]

        cleaned_data_mask = np.ones(self.input_data_shape, dtype='bool')
        cleaned_data_mask[self.pp_roi_image_cube_index] = False

        return cleaned_data, cleaned_data_uncertainty, cleaned_data_mask

    def return_filtered_data(self):
        """
        Returns filtered data set.

        Returns
        -------
        filtered_data : 'ndarray' of 'float'
            Optimally filtered (smoothed) data cube
        filtered_data_uncertainty : 'ndarray' of 'float'
            Uncertainty on the optimally filtered data cube.
        filtered_data_mask : 'ndarray' of 'bool'
            Pixel mask of the optimally filtered data cube.

        """
        optimal_filtered_data = np.zeros(self.input_data_shape)
        optimal_filtered_data[self.pp_roi_image_cube_index] = \
            self.optimal_filtered_image_cube[self.pp_data_cube_valid_index]


        optimal_filtered_data_uncertainty = np.zeros(self.input_data_shape)
        optimal_filtered_data_uncertainty[self.pp_roi_image_cube_index] = \
            np.sqrt(self.optimal_filtered_variance[self.pp_data_cube_valid_index])

        optimal_filtered_data_mask = np.ones(self.input_data_shape, dtype='bool')
        optimal_filtered_data_mask[self.pp_roi_image_cube_index] = False

        return (optimal_filtered_data, optimal_filtered_data_uncertainty,
                optimal_filtered_data_mask)

    def return_updated_mask(self):
        """
        Returns bad pixel flagged data mask.

        Returns
        -------
        updated_data_mask : 'ndarray' of 'bool'
            Bad pixel mask of the input data set, updated for bad pixels.

        """

        updated_data_mask = np.ones(self.input_data_shape, dtype='bool')
        updated_data_mask[self.pp_roi_image_cube_index]  = \
            ~self.cumulative_image_cube_mask[self.pp_data_cube_valid_index].astype(bool)

        return updated_data_mask


class EdgeFilter:
    """
    Edge filter to determine source location and region of interest.

    """

    def __init__(self, configuration_file='edge_filter.conf',
                 path=CONFIG_PATH):
        self.configuration_files = \
                self.check_configuration_files(configuration_file, path)
        self.configuration = \
                self.read_configuration_files(self.configuration_files)

        self.filter_kernels = \
            self.load_filter_kernels(self.configuration["filter_kernel"],
                                     self.configuration["filter_kernel_size"])
        try:
            self.filtering_results
        except AttributeError:
            self.filtering_results = SimpleNamespace()
        try:
            self.data
        except AttributeError:
            self.data = SimpleNamespace()
        try:
            self.source_location
        except AttributeError:
            self.source_location = SimpleNamespace()

    @staticmethod
    def check_configuration_files(configuration_file, path):
        """
        Check ic configuration file excist.

        Parameters
        ----------
        configuration_file : 'str'
            Configuration file name
        path : 'str' or pathlib.Path
            Path to the configuration file.

        Raises
        ------
        FileNotFoundError
            Error raised if file not found

        Returns
        -------
        file_path : 'str'
            Checked location of configuration file.

        """
        file_path = pathlib.Path(path) / configuration_file
        if not file_path.is_file:
            raise FileNotFoundError('Configureation file not found')
        return str(file_path)

    @staticmethod
    def read_configuration_files(*files):
        """
        Read .ini files using the configparser package.

        Parameters
        ----------
        files : 'list' of 'str'
            List of file names of initialization files to be read to initialize
            an instance of a TSO object.

        Raises
        ------
        ValueError
            An error is raised if the configuration file can not be found.
        """
        parser = configparser.ConfigParser()
        parser.optionxform = str  # make option names case sensitive
        found = parser.read(files)
        if not found:
            raise ValueError('Config file not found!')

        parameters = {}
        section_names = parser.sections()
        for name in section_names:
            parameters.update(parser.items(name))
        for k, v in parameters.items():
            parameters[k] = ast.literal_eval(v)
        return parameters

    def load_filter_kernels(self, filter_kernel: str, kernel_size: int):
        """
        Load derivative filter kernel stack.

        Parameters
        ----------
        filter_kernel : str
            Name of the filter kernel stack.
        kernel_size : int
            Size in pixels of the filter kernel

        Raises
        ------
        ValueError
            Is raised if name of filter kernel is not recognized.

        Returns
        -------
        filter_kernel : 'ndarray'
            Derivative filter kernel stack

        """
        _valid_kernels = {'Sobel':create_sobel_kernels,
                          'Schar':create_schar_kernels}
        if filter_kernel in _valid_kernels.keys():
            return _valid_kernels[filter_kernel](kernel_size=kernel_size)
        else:
            raise ValueError('Derivative kernel not valid.')

    def run_filter(self, image_cube: np.ndarray, mask_cube: np.ndarray) -> None:
        """
        Run edge filter.

        Parameters
        ----------
        image_cube : np.ndarray
            Input data cube.
        mask_cube : np.ndarray
            Mask of input data cube.

        Returns
        -------
        None.

        """
        self.preprocess_data(image_cube, mask_cube)
        self.derivative_filter(self.configuration["filter_verbose"])
        self.nm_suppression(self.configuration["filter_verbose"])
        self.threshold(self.configuration["filter_verbose"])
        self.hysteresis(self.configuration["filter_verbose"])

    def derive_source_location(self) -> None:
        """
        Run all functions to derive source location and masks.

        Returns
        -------
        None

        """
        self.create_target_masks(self.configuration["source_extraction_width"],
                                 self.configuration["extension_extraction_height"],
                                 self.configuration["filter_verbose"])
        self.determine_source_center(self.configuration["source_treshold"],
                                     self.configuration["filter_verbose"])

    def preprocess_data(self, image_cube: np.ndarray, mask_cube: np.ndarray) -> None:
        """
        Preprocess data befor edge filtering.

        Parameters
        ----------
        image_cube : 'numpy.ndarray' of 'float'
            Input spectral data cube
        mask_cube : 'numpy.ndarray' of 'bool'
            Input data mask (uses numpy masked array convention)

        Returns
        -------
        None
            DESCRIPTION.

        """
        # Gaussian smoothing
        kernel = create_gaussian_kernel(
        self.configuration["pre_process_kernel_size"],
        self.configuration["pre_process_gaussian_sigma"]
        )
        kernel = kernel[None, ...]
        (pp_image_cube, pp_mask_cube, _, pp_roi_image_cube_index ,
         pp_data_cube_valid_index, filtered_data_valid_index) = \
            prepare_data_for_filtering(image_cube, mask_cube,
                                       kernel_stack_shape=kernel.shape
                                       )

        filtered_image_cube = \
            filter_image_cube(pp_image_cube, pp_mask_cube,  kernel)
        filtered_image_cube = \
            filtered_image_cube[filtered_data_valid_index][0, ...]

        # add border for sobel/char filter.
        (self.data.pp_image_cube, _, _, self.data.pp_roi_image_cube_index ,
         self.data.pp_data_cube_valid_index, self.data.filtered_data_valid_index) = \
            prepare_data_for_filtering(filtered_image_cube,
                                       kernel_stack_shape=self.filter_kernels.shape,
                                       pad_mode='reflect')

    def derivative_filter(self, verbose: bool = False) -> None:
        """
        Calculate the magnitude and angle of the partial derivative.

        Parameters
        ----------
        verbose : 'bool'
            If true saves intermediate results.

        Returns
        -------
        None

        """
        # Jacobinan
        J = np.zeros(self.data.pp_image_cube.shape+(2,))
        # (dI/dx, dI/dy)
        J[..., 0:2] = \
           np.moveaxis(filter_image_cube_edge_detection(self.data.pp_image_cube,
                                                        self.filter_kernels), 0, 3)

        G = np.hypot(J[..., 0], J[..., 1])
        G = (G.T / G.T.max(axis=(0,1))).T * 255
        theta = np.arctan2(J[..., 1], J[..., 0])
        theta = np.rad2deg(theta)
        theta[theta<0.0] += 180.0
        theta[theta+1.e-8 > 180.0] = 0.0

        # Hessian
        H = np.zeros(self.data.pp_image_cube.shape+(2,2,))
        # (Hxx, Hyx)
        H[..., 0:2, 0] = np.moveaxis(filter_image_cube_edge_detection(J[..., 0],
                                     self.filter_kernels), 0, 3)
        # (Hxy, Hyy)
        H[..., 0:2, 1] = np.moveaxis(filter_image_cube_edge_detection(J[..., 1],
                                     self.filter_kernels), 0, 3)

        # max absolute eigen vector eand value
        W, v = np.linalg.eig(H)
        idx = np.argmax(np.abs(W.real), axis=-1)
        dim1, dim2, dim3 = idx.shape
        grid1, grid2, grid3 = np.ogrid[:dim1,:dim2,:dim3]
        e_value_max = W[grid1, grid2, grid3, idx].real
        e_vector_max = -v[grid1, grid2, grid3, :, idx].real

        # second order taylor expansion in direction of max vlue eigen vector
        # to determine maximum of second order derivative, i.e. maximum of the
        # spectral trace.
        extrema_distance = \
            -1 * (e_vector_max[..., 0] * J[..., 0] +
                  e_vector_max[..., 1] * J[..., 1]) / \
                (e_vector_max[..., 0]**2 * H[..., 0, 0] +
                 2 * e_vector_max[..., 0] *
                 e_vector_max[..., 1] * H[..., 0, 1] +
                 e_vector_max[..., 1]**2 * H[..., 1, 1] + 1.e-14)
        extrema_vector = (e_vector_max.T*extrema_distance.T).T

        trace_angle = \
            np.arctan(e_vector_max[..., 0] / (e_vector_max[..., 1] + 1.e-14))
        trace_angle = trace_angle%(2*np.pi)
        trace_angle[trace_angle >= np.pi] -= np.pi

        self.filtering_results.hessian = H
        self.filtering_results.extrema_vector = extrema_vector
        self.filtering_results.trace_angle = trace_angle
        self.filtering_results.filtered_cube = G
        self.filtering_results.filtered_angle_cube = theta

        if verbose:
            self.filtering_results.edge_cube = G.copy()
            self.filtering_results.angle_cube = theta.copy()
            self.filtering_results.eigen_value_max = e_value_max
            self.filtering_results.eigen_vector_max = e_vector_max
            self.filtering_results.extrema_distance = extrema_distance
            self.filtering_results.jacobian = J
            self.filtering_results.eigen_values = W.real
            self.filtering_results.eigen_vectors = v.real


    def nm_suppression(self, verbose: bool = False) -> None:
        """
        Non local maximum suppression.

        Parameters
        ----------
        verbose : 'bool'
            If true saves intermediate results.

        Returns
        -------
        None

        """
        nms_edge_cube = \
            non_max_suppression(self.filtering_results.filtered_cube,
                                self.filtering_results.filtered_angle_cube)

        self.filtering_results.filtered_cube = nms_edge_cube
        if verbose:
            self.filtering_results.nms_edge_cube = nms_edge_cube.copy()

    def threshold(self, verbose: bool = False) -> None:
       """
        Double tresholding.

        Parameters
        ----------
        verbose : 'bool'
            If true saves intermediate results.

        Returns
        -------
        None

        """
       high_threshold = \
           (self.filtering_results.filtered_cube.max() *
            self.configuration["high_threshold_ratio"])
       low_threshold = \
           (high_threshold * self.configuration["low_threshold_ratio"])

       T, M, N = self.filtering_results.filtered_cube.shape
       res = np.zeros((T, M, N), dtype=np.int32)

       weak = np.int32(25)
       strong = np.int32(255)
       strong_k, strong_i, strong_j = \
           np.where(self.filtering_results.filtered_cube >= high_threshold)
       zeros_k, zeros_i, zeros_j = \
           np.where(self.filtering_results.filtered_cube < low_threshold)
       weak_k, weak_i, weak_j = \
           np.where((self.filtering_results.filtered_cube <= high_threshold) &
                    (self.filtering_results.filtered_cube >= low_threshold))

       res[strong_k, strong_i, strong_j] = strong
       res[weak_k, weak_i, weak_j] = weak

       self.filtering_results.filtered_cube = res
       if verbose:
           self.filtering_results.tresholed_image_cube = res.copy()
       self.filtering_results.weak = weak
       self.filtering_results.strong = strong

    def hysteresis(self, verbose: bool = False) -> None:
        """
        Hysteresis.

        Parameters
        ----------
        verbose : 'bool'
            If true saves intermediate results.

        Returns
        -------
        None

        """
        canny_image_cube = self.filtering_results.filtered_cube.copy()
        not_converged = True
        total = int(np.sum(canny_image_cube))
        while not_converged:
            canny_image_cube += \
                filter_hysteresis(canny_image_cube, self.filtering_results.weak,
                                  self.filtering_results.strong)
            canny_image_cube[canny_image_cube>255] = 255
            total_new = int(np.sum(canny_image_cube))
            if total_new == total:
                not_converged = False
            else:
                total = total_new
        canny_image_cube = \
            filter_hysteresis(canny_image_cube, self.filtering_results.weak,
                              self.filtering_results.strong)

        canny_image_cube = canny_image_cube[self.data.pp_data_cube_valid_index]

        self.filtering_results.filtered_cube = canny_image_cube
        if verbose:
            self.filtering_results.canny_image_cube = canny_image_cube.copy()

    def create_target_masks(self, extraction_width : int = 15,
                            extension_extraction_height: int = 2,
                            verbose: bool = False) -> None:
        """
        Create extraction masks for each target.

        Returns
        -------
        None

        """
        source_mask = self.filtering_results.filtered_cube > 0

        source_mask = \
            ndimage.binary_closing(source_mask,
                                              structure=np.ones((1, 1, 10)))

        source_mask = \
            ndimage.binary_dilation(
                source_mask, structure=np.ones((1, extension_extraction_height,
                                                (2*extraction_width-16)//2)))

        s = ndimage.generate_binary_structure(3,2)
        labeled_source_mask, num_sources = ndimage.label(source_mask ,structure=s)
        source_list = ndimage.find_objects(labeled_source_mask)

        source_mask = np.zeros((num_sources,)+source_mask.shape, dtype='bool')
        for itarget in range(num_sources):
            source_mask[itarget, ...] = labeled_source_mask == itarget+1

        roi = np.zeros((len(source_list),)+source_mask.shape[2:], dtype='bool')
        for itarget, slices in enumerate(source_list):
            temp_mask = np.zeros_like(source_mask[itarget, ...], dtype=bool)
            temp_mask[slices] = True
            roi[itarget, ...] = temp_mask.any(axis=0)

        if verbose:
            self.source_location.sources = source_list
        self.source_location.roi = ~roi
        self.source_location.source_mask = ~source_mask
        self.source_location.number_of_sources = num_sources

    def determine_source_center(self, relative_source_treshold: float = 0.01,
                                verbose: bool = False) -> None:
        """
        Determine the center if the dispersed light (spectral trace).

        Parameters
        ----------
        relative_source_treshold : float, optional
            Reletave level of hessian trace value below which data is rejected.
            The default is 0.01.
        verbose : bool, optional
            If true saves addition output. The default is False.

        Returns
        -------
        None

        Notes
        -----
        We use the convention (X, Y) for the image coordinates. Note that the
        pytthon converntion for array indicii is [Y, X]. So coordinate
        (10, 20) is the center of pixel[20, 10],

        """
        hessian = np.zeros(self.source_location.source_mask.shape[1:]+(2,2,))
        hessian[...,0,0] = \
            self.filtering_results.hessian[..., 0, 0][self.data.pp_data_cube_valid_index]
        hessian[...,0,1] = \
            self.filtering_results.hessian[..., 0, 1][self.data.pp_data_cube_valid_index]
        hessian[...,1,0] = \
            self.filtering_results.hessian[..., 1, 0][self.data.pp_data_cube_valid_index]
        hessian[...,1,1] = \
            self.filtering_results.hessian[..., 1, 1][self.data.pp_data_cube_valid_index]

        i0, i1 = np.ogrid[:hessian.shape[0],:hessian.shape[1]]
        index_hessian_minimum = \
            np.argmin(
                np.trace(
                    hessian, axis1=-2, axis2=-1),
                axis=-1)

        tr_h = np.trace(-hessian, axis1=-2, axis2=-1)
        tr_h = tr_h/np.max(tr_h)*255
        trace_mask = \
            np.zeros((self.source_location.roi.shape[0:1]+hessian.shape[0:3]),
                     dtype=bool)

        for isource, roi in enumerate(self.source_location.roi):
            trace_mask[isource, i0, i1, index_hessian_minimum] = True
            trace_mask[isource, :, roi] = False
            trace_mask[isource, tr_h < (relative_source_treshold*255)] = False
        trace_mask = ~trace_mask

        Xvector = \
            self.filtering_results.extrema_vector[..., 0][self.data.pp_data_cube_valid_index]
        Yvector = \
            self.filtering_results.extrema_vector[..., 1][self.data.pp_data_cube_valid_index]

        source_traces = []
        for mask in ~trace_mask:
            source_traces_per_integration = []
            for i, sub_mask in enumerate(mask):
                #X = Xvector[mask[sub_mask]]+np.where(mask[])[2]
                X =  Xvector[i, sub_mask] + np.where(sub_mask)[1]
                #Y = Yvector[mask]+np.where(mask)[1]
                Y = Yvector[i, sub_mask] + np.where(sub_mask)[0]
                #index_in_pixel = (Xvector[mask] < 0.50)  & (Yvector[mask] < 0.50)
                index_in_pixel = (Xvector[i, sub_mask] < 0.50)  & (Yvector[i, sub_mask] < 0.50)
                #source_traces.append((X[index_in_pixel], Y[index_in_pixel]))
                source_traces_per_integration.append((X[index_in_pixel], Y[index_in_pixel]))
            source_traces.append(source_traces_per_integration)

        self.source_location.trace_mask = trace_mask
        self.source_location.source_traces = source_traces
        if verbose:
            pass

