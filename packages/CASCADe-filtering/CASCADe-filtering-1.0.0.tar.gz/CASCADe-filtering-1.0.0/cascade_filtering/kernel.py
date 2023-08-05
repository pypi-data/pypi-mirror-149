#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 21:12:13 2022

@author: bouwman
"""
import math
import numpy as np
import warnings
import configparser
import pathlib
import os
import ast
from typing import Union
from scipy.spatial.transform import Rotation as R
from scipy.stats import multivariate_normal
from astropy.convolution import Kernel2D
from astropy.convolution import Gaussian2DKernel
from astropy.modeling.models import Gaussian2D
from astropy.modeling.parameters import Parameter
from cascade_filtering.stencil import IMPLEMENTED_KERNEL_SIZES
from cascade_filtering import __path__

__all__ = ['FilterKernel', 'create_anisotropic_curved_kernels',
           'create_nagano_matsuyama_kernels', 'create_kuwahara_kernels',
           'define_covariance_matrix', 'define_anisotropic_gaussian_kernel',
           'create_square_kernels', 'create_sift_kernels',
           'create_gaussian_kernel']

CONFIG_PATH = pathlib.Path(os.path.dirname(__path__[0])) / 'configuration_files/'

def _round_up_to_odd_integer(value):
    """
    Round to odd integer.

    Parameters
    ----------
    value : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    i = math.ceil(value)
    if i % 2 == 0:
        return i + 1
    return i


class Banana(Gaussian2D):
    """
    Modification of astropy gaussian2D to get banana distribution.

    Notes
    -----
    https://tiao.io/post/building-probability-distributions-
    with-tensorflow-probability-bijector-api/
    """

    amplitude = Parameter(default=1)
    x_mean = Parameter(default=0)
    y_mean = Parameter(default=0)
    x_stddev = Parameter(default=1)
    y_stddev = Parameter(default=1)
    theta = Parameter(default=0.0)
    power = Parameter(default=1.0)
    sign = Parameter(default=1)

    def __init__(self, amplitude=amplitude.default, x_mean=x_mean.default,
                 y_mean=y_mean.default, x_stddev=None, y_stddev=None,
                 theta=None, cov_matrix=None, power=power.default,
                 sign=sign.default, **kwargs):
        if power is None:
            power = power.default
        if sign is None:
            sign = sign.default
        sign = np.sign(sign)
        super().__init__(
            amplitude=amplitude, x_mean=x_mean, y_mean=y_mean,
            x_stddev=x_stddev, y_stddev=y_stddev, theta=theta,
            cov_matrix=cov_matrix, power=power, sign=sign, **kwargs)

    @staticmethod
    def evaluate(x_in, y_in, amplitude, x_mean, y_mean, x_stddev, y_stddev,
                 theta, power, sign):
        """Two dimensional Gaussian function."""
        x = x_in
        y = y_in - sign*(np.abs(x_in)**power + 0.0)
        cost2 = np.cos(theta) ** 2
        sint2 = np.sin(theta) ** 2
        sin2t = np.sin(2. * theta)
        xstd2 = x_stddev ** 2
        ystd2 = y_stddev ** 2
        xdiff = x - x_mean
        ydiff = y - y_mean
        a = 0.5 * ((cost2 / xstd2) + (sint2 / ystd2))
        b = 0.5 * ((sin2t / xstd2) - (sin2t / ystd2))
        c = 0.5 * ((sint2 / xstd2) + (cost2 / ystd2))
        return amplitude * np.exp(-((a * xdiff ** 2) + (b * xdiff * ydiff) +
                                    (c * ydiff ** 2)))


class Banana2DKernel(Kernel2D):
    """
    Modification of astropy Gaussian2DKernel to get a banana shaped kernel.

    This class defines a banana shaped convolution kernel mimicking the shape
    of the dispersion pattern on the detector near the short and long
    wavelength ends.
    """

    _separable = True
    _is_bool = False

    def __init__(self, sigma, power=None, sign=None, **kwargs):
        self._model = Banana(1. / (2 * np.pi * sigma[0, 0] * sigma[1, 1]),
                             0., 0., cov_matrix=sigma, power=power, sign=sign)
        self._default_size = _round_up_to_odd_integer(
            8 * np.max([np.sqrt(sigma[0, 0]), np.sqrt(sigma[1, 1])]))
        super().__init__(**kwargs)
        self._truncation = np.abs(1. - self._array.sum())


def define_covariance_matrix(sigma=[1.0, 1.0, 1.0], theta=[0.0], degrees=False):
    """
    Define covariance matrix.

    Define 2D covariance matrix based on the standard deviation in the
    dispersion and cross-dispersion direction, or the 3D covariance matrix
    including the standard deviation in the time direction. Rotation angles
    can be specified to indicate either a rotation in the dispersion -
    cross-dispersion plane (2D and 3D), or around all axis (3D).

    Parameters
    ----------
    sigma : 'list' of float or int, or int or float
        Standard deviation of the Gaussian Kernel
    theta : 'list' of float or int, or int or float

    Raises
    ------
    ValueError
        An error is raised if the sigam and theta specifications are
        inconsistent with a 2D or 3D Gaussian Kernel.
    """
    if not isinstance(sigma, list):
        if isinstance(sigma, (int, float)):
            sigma = [sigma]
        else:
            raise ValueError("Input sigma of wrong type")
    if len(sigma) == 1:
        # simple symmetric 2D gaussian kernel
        covariance_matrix = np.diag(sigma + sigma)**2
    elif len(sigma) in [2, 3]:
        # standard 2d or 3D kernel
        covariance_matrix = np.diag(sigma)**2
    else:
        # to many sigma's
        raise ValueError("input list of sigma's to long.")


    if not isinstance(theta, list):
        if isinstance(theta, (int, float)):
            theta = [theta]
        else:
            raise ValueError("Input sigma of wrong type")
    if covariance_matrix.shape == (2,2):
        #  2D covariance with rotation
        if len(theta) == 1:
        # rotation only in XY plain.
            rotation_vector =  [0, 0] + theta
        else:
            raise ValueError("2D kernel can only have 1 rotaton angle")
    else:
        if len(theta) == 1:
        # rotation only in XY plain.
            rotation_vector = [0, 0] + theta
        elif len(theta) == 3:
            rotation_vector = theta
        else:
            raise ValueError("defination of rotation angles not consistent "
                             "with 3D Kernel")
    rotation_matrix = define_rotation_matrix(rotation_vector, degrees=degrees)
    rotation_matrix = rotation_matrix[-covariance_matrix.shape[0]:,
                                      -covariance_matrix.shape[1]:]
    covariance_matrix = np.linalg.multi_dot([rotation_matrix,
                                             covariance_matrix,
                                             rotation_matrix.T])
    return covariance_matrix


def define_rotation_matrix(theta=[0.0, 0.0, 0.0], degrees=True):
    """
    Created 3D rotation matrix

    Parameters
    ----------
    theta : TYPE, optional
        DESCRIPTION. The default is [0.0, 0.0, 0.0].
    degrees : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    rotation_matrix : TYPE
        DESCRIPTION.

    """
    rotation_matrix = R.from_euler('zyx', theta, degrees=degrees).as_matrix()
    return rotation_matrix


def define_anisotropic_gaussian_kernel(kernel_shape: tuple,
                                       sigma: Union[list, int, float],
                                       theta: Union[list, int, float],
                                       degrees=True) -> np.ndarray:
    """
    Define the anisitropic gaussian kernel.

    Parameters
    ----------
    kernel_shape : tuple
        DESCRIPTION.
    sigma : Union[list, int, float]
        DESCRIPTION.
    theta : Union[list, int, float]
        DESCRIPTION.
    degrees : TYPE, optional
        DESCRIPTION. The default is True.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    kernel : TYPE
        DESCRIPTION.

    """
    n_oversample = 11
    kernel_dimension = len(kernel_shape)
    if not kernel_dimension in [2,3]:
        raise ValueError("kernel shape inconsistent with 2D or 3D kernel.")
    if np.unique(kernel_shape).size != 1:
        raise ValueError("kernel shape inconsistent with square or cube "
                             "shaped kernel.")
    kernel_size = kernel_shape[0]

    half_width = (kernel_size*n_oversample)//2

    if not isinstance(sigma, list):
        if isinstance(sigma, (int, float)):
            sigma = [sigma]
        else:
            raise ValueError("Input sigma of wrong type")
    oversampled_sigma = [mu*n_oversample for mu in sigma]


    if kernel_dimension == 2:

        x = np.arange(-half_width, half_width+1)
        y = np.arange(-half_width, half_width+1)

        X, Y = np.meshgrid(x,y, indexing='xy')

        grid_positions = np.empty(X.shape + (2,))

        grid_positions[..., 0] = Y
        grid_positions[..., 1] = X

        rebin_tuple = (kernel_size, n_oversample, kernel_size,
                       n_oversample)
        rebin_axis_tuple = (1,3)

    else:

        x = np.arange(-half_width, half_width+1)
        y = np.arange(-half_width, half_width+1)
        z = np.arange(-half_width, half_width+1)

        X, Y, Z = np.meshgrid(x,y,z, indexing='xy')

        grid_positions = np.empty(X.shape + (3,))
        grid_positions[..., 0] = Y
        grid_positions[..., 1] = X
        grid_positions[..., 2] = Z

        rebin_tuple = (kernel_size, n_oversample, kernel_size,
                       n_oversample, kernel_size, n_oversample)
        rebin_axis_tuple = (1,3,5)


    covariance_matrix = define_covariance_matrix(sigma=oversampled_sigma,
                                                 theta=theta,
                                                 degrees=degrees)
    center_position = np.zeros((kernel_dimension))
    rv = multivariate_normal(center_position, covariance_matrix)

    kernel = rv.pdf(grid_positions)
    kernel = np.mean(kernel.reshape(rebin_tuple), axis=rebin_axis_tuple)
    kernel /= np.sum(kernel)

    return kernel


def create_anisotropic_curved_kernels(kernel_size=9) -> np.ndarray:
    """
    Directional filters for smoothing and filtering.

    These filters can be used in a Nagao&Matsuyama like edge preserving
    smoothing approach and are apropriate for dispersed spectra with a
    vertical dispersion direction. If the angle from vertical of the
    spectral trace of the dispersed light exceeds +- max(angle) radians,
    additional larger values need to be added to the angles list.

    Parameters
    ----------
    kernel_size : 'int'
        Size of 2d kernel

    Returns
    -------
    kernel_stack : numpy.ndarray of 'float'
        Array containing all oriented filter kernels used for edge
        preserving smooting.

    Notes
    -----
    When adding kernels, make sure the maximum is in the central pixel
    """
    # note that the angels are in radians
    angles = [np.radians(0.0), np.radians(-1.5), np.radians(1.5),
              np.radians(-3.0), np.radians(3.0), np.radians(-4.5),
              np.radians(4.5), np.radians(-6.0), np.radians(6.0),
              np.radians(-9.0), np.radians(9.0), np.radians(-12.0),
              np.radians(12.0),
              np.radians(0.0),
              np.radians(90)-np.radians(60), np.radians(90)+np.radians(60),
              np.radians(90)-np.radians(60), np.radians(90)+np.radians(60)]

    x_stddev = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                0.1, 0.1, 0.1, 0.1,
                2.0,
                0.1, 0.1, 0.1, 0.1]
    y_stddev = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
                3.0, 3.0, 3.0, 3.0,
                2.0,
                3.0, 3.0, 3.0, 3.0]
    sign = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0,
            1, 1, -1, -1]
    power = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0,
             0.0,
             1.0, 1.0, 1.0, 1.0]

    x_kernel_size = kernel_size
    y_kernel_size = kernel_size

    kernel_stack = np.zeros((len(angles), x_kernel_size, y_kernel_size))

    for ik, (omega, xstd, ystd, p, s) in enumerate(zip(angles, x_stddev,
                                                       y_stddev, power, sign)):
        sigma = define_covariance_matrix([xstd, ystd], [omega])
        kernel = Banana2DKernel(sigma, x_size=x_kernel_size,
                                y_size=y_kernel_size, power=p, sign=s,
                                mode='oversample')
        kernel.normalize()
        kernel_stack[ik, ...] = kernel.array

    return kernel_stack


def create_gaussian_kernel(kernel_size:int = 7, sigma:float = 1.0):
    """
    Create gaussian kernel.

    Parameters
    ----------
    kernel_size : int, optional
        DESCRIPTION. The default is 7.
    sigma : float, optional
        DESCRIPTION. The default is 1.0.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    kernel = Gaussian2DKernel(x_stddev=sigma, y_stddev=sigma,
                              x_size=kernel_size, y_size=kernel_size)
    kernel.normalize()
    return kernel.array


def create_sift_kernels(kernel_size:int = 11) -> Union[np.ndarray, float, float]:
    """
    Create a kernel stack for SIFT.

    Parameters
    ----------
    kernel_size : int, optional
        DESCRIPTION. The default is 11.

    Returns
    -------
    kernel_stack : TYPE
        DESCRIPTION.
    s : TYPE
        DESCRIPTION.
    min_sigma : TYPE
        DESCRIPTION.

    """
    min_sigma = 0.5
    max_sigma = kernel_size/6.0
    n_kernels = kernel_size
    s = (max_sigma/min_sigma)**(1.0/(n_kernels-1))
    sigmas = [min_sigma*s**i for i in range(n_kernels)]

    kernel_stack = []
    for ik in range(n_kernels):
        kernel = Gaussian2DKernel(x_stddev=sigmas[ik], y_stddev=sigmas[ik],
                                  x_size=kernel_size, y_size=kernel_size)
        kernel.normalize()
        kernel_stack.append(kernel.array)
    kernel_stack = np.array(kernel_stack)
    return kernel_stack, s, min_sigma


def create_sobel_kernels(kernel_size : int = 3):
    if kernel_size == 3:
        Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)/8.
        Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)/8.
    else:
        Gx = np.array([[-5, -4, 0, 4, 5], [-8, -10, 0, 10, 8],
                       [-10, -20, 0, 20, 10], [-8, -10, 0, 10, 8],
                       [-5, -4, 0, 4, 5]], dtype=float)/240.
        Gy = np.array([[-5, -8, -10, -8, -5], [-4, -10, -20, -10, -4],
                       [0, 0, 0, 0, 0], [4, 10, 20, 10, 4],
                       [5, 8, 10, 8, 5]], dtype=float)/240.
    kernel_stack = []
    kernel_stack.append(Gx)
    kernel_stack.append(Gy)
    kernel_stack = np.array(kernel_stack)
    return kernel_stack


def create_schar_kernels(kernel_size : int = 3):
    if kernel_size == 3:
        Gx = np.array([[-1, 0, 1], [-3, 0, 3], [-1, 0, 1]], dtype=float)/10.
        Gy = np.array([[-1, -3, -1], [0, 0, 0], [1, 3, 1]], dtype=float)/10.
    else:
        Gx = np.array([[-1, -1, 0, 1, 1], [-2, -2, 0, 2, 2],
                       [-3, -6, 0, 6, 3], [-2, -2, 0, 2, 2],
                       [-1, -1, 0, 1, 1]], dtype=float)/60.
        Gy = np.array([[-1, -2, -3, -2, -1], [-1, -2, -6, -2, -1],
                       [0, 0, 0, 0, 0], [1, 2, 6, 2, 1],
                       [1, 2, 3, 2, 1]], dtype=float)/60.
    kernel_stack = []
    kernel_stack.append(Gx)
    kernel_stack.append(Gy)
    kernel_stack = np.array(kernel_stack)
    return kernel_stack


def create_square_kernels(kernel_size=11) -> np.ndarray:
    """
    Create stack of square kernels.

    Parameters
    ----------
    kernel_size : TYPE, optional
        Kernel size. The default is 9.

    Returns
    -------
    kernel_stack: 'ndarray'
        Kernel stack

    """
    kernel_stack = []
    for i in range(kernel_size//2):
        kernel_temp = np.full((kernel_size,  kernel_size), fill_value=0.0)
        kernel_temp[i:kernel_size-i, i:kernel_size-i] = 1.0
        kernel_stack.append(kernel_temp)
    kernel_stack = np.array(kernel_stack)

    return kernel_stack


def create_kuwahara_kernels(kernel_size=9) -> np.ndarray:
    """
    Create stack of Kuwahara kernels.

    Parameters
    ----------
    kernel_size : TYPE, optional
        DESCRIPTION. The default is 9.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    kernel = create_square_kernels(kernel_size=kernel_size)

    kernel2 = []
    for i in range(kernel_size//2):
        kernel_temp = np.full((kernel_size,  kernel_size), fill_value=0.0)
        kernel_temp[kernel_size//2:kernel_size-i, kernel_size//2:kernel_size-i] = 1.0
        kernel2.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=1)
        kernel2.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=0)
        kernel2.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=1)
        kernel2.append(kernel_temp)
    kernel2 = np.array(kernel2)

    return np.vstack([kernel, kernel2])


def create_nagano_matsuyama_kernels(kernel_size=9) -> np.ndarray:
    """
    Create and stack of nagano-matsuyama kernels.

    Parameters
    ----------
    kernel_size : TYPE, optional
        DESCRIPTION. The default is 9.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    kernel = create_square_kernels(kernel_size=kernel_size)

    kernel2 = []
    for i in range(kernel_size//2-1):
        kernel_temp = np.full((kernel_size,  kernel_size), fill_value=0.0)
        kernel_temp[kernel_size//2, kernel_size//2] = 1.0
        kernel_temp[kernel_size//2-1:kernel_size//2+2, kernel_size//2+1:kernel_size//2+3+i] = 1.0
        kernel2.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=1)
        kernel2.append(kernel_temp)
        kernel_temp = kernel_temp.T
        kernel2.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=0)
        kernel2.append(kernel_temp)
    kernel2 = np.array(kernel2)

    kernel3 = []
    for i in range(kernel_size//2-1):
        kernel_temp = np.full((kernel_size,  kernel_size), fill_value=0.0)
        for j in range(2+i):
            kernel_temp[kernel_size//2+j:kernel_size//2+2+j,
                        kernel_size//2+j:kernel_size//2+2+j] = 1.0
        kernel_temp = np.flip(kernel_temp, axis=1)
        kernel3.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=0)
        kernel3.append(kernel_temp)
        kernel_temp = np.flip(kernel_temp, axis=1)
        kernel3.append(kernel_temp)
    kernel3 = np.array(kernel3)

    return np.vstack([kernel, kernel2, kernel3])


class FilterKernel:

    def __init__(self, configuration_file='anisotropic_gaussian_kernel.conf',
                 path=CONFIG_PATH):
        self.configuration_files = \
            self.check_configuration_files(configuration_file, path)
        self.configuration = \
            self.read_configuration_files(self.configuration_files)
        self.used_kernel_model = self.check_kernel_models()
        self.kernel_stack = self.create_kernel_stack()()

    @staticmethod
    def check_configuration_files(configuration_file, path):
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

    @property
    def __valid_models(self):
        valid_model_dictionary =\
            {"anisotropic_gaussian": self.generate_anisotropic_gaussian_kernel,
             "banana": self.generate_banana_kernel,
             "kuwahara": self.generate_kuwahara_kernel,
             "nagano_matsuyama": self.generate_nagano_matsuyama_kernel
        }
        return valid_model_dictionary

    @staticmethod
    def check_angles(min_angle, max_angle, number_of_angles):
        if max_angle < min_angle:
            raise ValueError("The maximum angle should be larger than the "
                             "mininmum angle.")
        if np.abs(max_angle - min_angle) > 180.0:
            raise ValueError("The maximum angle range should not be larger "
                             "than 180 degrees.")
        if number_of_angles%2 - 1:
            warnings.warn("Number angles should be odd, adding 1")
            number_of_angles += 1
        return True

    @staticmethod
    def check_kernel_shape(kernel_shape):

        valid_2d_shapes = [(i, i) for i in IMPLEMENTED_KERNEL_SIZES]
        valid_3d_shapes = [(i, i, i) for i in IMPLEMENTED_KERNEL_SIZES]

        if not ((kernel_shape in valid_2d_shapes) |
                (kernel_shape in valid_3d_shapes)):
            raise ValueError("Kernel size not implemented. The following "
                             f"sizes can be used: {IMPLEMENTED_KERNEL_SIZES}."
            )

        kernel_size = kernel_shape[0]
        kernel_dimension = len(kernel_shape)

        return kernel_size, kernel_dimension

    @staticmethod
    def check_kernel_std(wavelength_stdev, spatial_stdev,
                         time_stdev=None):
        """
        Check the limits of the standard deviation of the used kernel.

        Parameters
        ----------
        wavelength_stdev : TYPE
            DESCRIPTION.
        spatial_stdev : TYPE
            DESCRIPTION.
        time_stdev : TYPE, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if wavelength_stdev < 0.2:
            raise ValueError("STDEV in wavelength direction to small")
        if spatial_stdev < 0.2:
            raise ValueError("STDEV in cross dispersion direction to small")
        if not time_stdev is None:
            if time_stdev < 0.2:
                raise ValueError("STDEV in time (integration) direction to small")
        return True

    def check_kernel_models(self):
        if not self.configuration['kernel_name'] in  self.__valid_models.keys():
            raise ValueError("Kernel model not valid.")
        return self.configuration['kernel_name']

    def generate_kuwahara_kernel(self):
        kernel_size, kernel_dimension = \
            self.check_kernel_shape(self.configuration['kernel_shape'])
        kernel_stack = create_kuwahara_kernels(kernel_size=kernel_size)
        return kernel_stack

    def generate_nagano_matsuyama_kernel(self):
        kernel_size, kernel_dimension = \
            self.check_kernel_shape(self.configuration['kernel_shape'])
        kernel_stack = create_nagano_matsuyama_kernels(kernel_size=kernel_size)
        return kernel_stack

    def generate_banana_kernel(self):
        kernel_size, kernel_dimension = \
            self.check_kernel_shape(self.configuration['kernel_shape'])
        kernel_stack = create_anisotropic_curved_kernels(kernel_size=kernel_size)
        return kernel_stack

    def generate_anisotropic_gaussian_kernel(self):
        """
        Generate an anisotropic gaussian kernel

        Returns
        -------
        kernel_stack : TYPE
            DESCRIPTION.

        """
        kernel_size, kernel_dimension = \
            self.check_kernel_shape(self.configuration['kernel_shape'])

        kernel_stack = \
            np.zeros((self.configuration['kernel_rotation_angles']['ntheta'],) +
                     self.configuration['kernel_shape']
                     )

        theta_min = self.configuration['kernel_rotation_angles']['theta_min']
        theta_max = self.configuration['kernel_rotation_angles']['theta_max']
        ntheta = self.configuration['kernel_rotation_angles']['ntheta']
        self.check_angles(theta_min, theta_max, ntheta)
        filter_angles = np.radians(np.linspace(theta_min, theta_max, ntheta))

        x_stddev = self.configuration['kernel_sigma']['sigma_crossdispersion']
        y_stddev = self.configuration['kernel_sigma']['sigma_dispersion']
        if  kernel_dimension == 3:
            z_stddev = self.configuration['kernel_sigma']['sigma_time']
            self.check_kernel_std(y_stddev, x_stddev, time_stdev=z_stddev)
            sigma = [z_stddev, y_stddev, x_stddev]
        else:
            self.check_kernel_std(y_stddev, x_stddev)
            sigma = [y_stddev, x_stddev]

        for ik, omega in enumerate(filter_angles):
            kernel = \
                define_anisotropic_gaussian_kernel(
                    self.configuration['kernel_shape'], sigma=sigma,
                    theta=[omega], degrees=False)

            kernel_stack[ik, ...] = kernel

        if self.configuration['kernel_add_endpoints']:

            omega_endpoints = [0.0, -60.0, -45.0, 45.0, 60.0, 90.0]
            x_stddev_endpoint = [2.0,] +  [x_stddev,]*5
            y_stddev_endpoint = [2.0,] + [y_stddev,]*5

            if  kernel_dimension == 3:
                z_stddev_endpoint = [z_stddev, ]*6
                sigma_endpoint = [[z,y,x] for z,y,x in zip(z_stddev_endpoint,
                                                           y_stddev_endpoint,
                                                           x_stddev_endpoint)]
            else:
                sigma_endpoint = [[y,x] for y,x in zip(y_stddev_endpoint,
                                                       x_stddev_endpoint)]

            kernel_stack_endpoint = np.zeros((len(omega_endpoints),) +
                                             self.configuration['kernel_shape']
                     )

            for ik, (omega, sigma) in enumerate(zip(omega_endpoints, sigma_endpoint)):
                   kernel = \
                       define_anisotropic_gaussian_kernel(
                           self.configuration['kernel_shape'], sigma=sigma,
                           theta=[omega], degrees=True)
                   kernel_stack_endpoint[ik, ...] = kernel

            kernel_stack = np.vstack([kernel_stack, kernel_stack_endpoint])
        return kernel_stack

    def create_kernel_stack(self):
        """
        Generate an kernel stack.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        command_generator = self.__valid_models
        return command_generator[self.used_kernel_model]
