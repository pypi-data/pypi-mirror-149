#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:59:44 2022

@author: bouwman
"""

import numpy as np
import numba as nb

_all__ = ['stencil_kernel3', 'stencil_kernel5', 'stencil_kernel7',
          'stencil_kernel9','stencil_kernel11', 'stencil_kernel19',
          'stencil_kernel5_3d', 'stencil_kernel7_3d',
          'stencil_kernel9_3d','stencil_kernel11_3d', 'stencil_kernel19_3d'
          'filter_image_cube', 'stencil_kernel_ufunc',
          'filter_image_cube_ufunc', 'stencil_kernel_3d_ufunc',
          'IMPLEMENTED_KERNEL_SIZES',
          'stencil_non_max_suppression',
          'stencil_non_max_suppression_ufunc','non_max_suppression',
          'filter_image_cube_edge_detection', 'filter_hysteresis']

IMPLEMENTED_KERNEL_SIZES = [3, 5, 7, 9, 11, 19]

@nb.stencil(neighborhood = ((-1, 1),(-1, 1)), standard_indexing=("kernel",))
def stencil_kernel3(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-1, 2):
        for j in range(-1, 2):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+1, j+1]
            norm_kernel += mask[i, j] * kernel[i+1, j+1]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-1, 1),(-1, 1),(-1, 1)), standard_indexing=("kernel",))
def stencil_kernel3_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+1, j+1, k+1]
               norm_kernel += mask[i, j, k] * kernel[i+1, j+1, k+1]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-2, 2),(-2, 2)), standard_indexing=("kernel",))
def stencil_kernel5(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-2, 3):
        for j in range(-2, 3):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+2, j+2]
            norm_kernel += mask[i, j] * kernel[i+2, j+2]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-2, 2),(-2, 2),(-2, 2)), standard_indexing=("kernel",))
def stencil_kernel5_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-2, 3):
        for j in range(-2, 3):
            for k in range(-2, 3):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+2, j+2, k+2]
               norm_kernel += mask[i, j, k] * kernel[i+2, j+2, k+2]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-3, 3),(-3, 3)), standard_indexing=("kernel",))
def stencil_kernel7(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-3, 4):
        for j in range(-3, 4):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+3, j+3]
            norm_kernel += mask[i, j] * kernel[i+3, j+3]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-3, 3),(-3, 3),(-3, 3)), standard_indexing=("kernel",))
def stencil_kernel7_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-3, 4):
        for j in range(-3, 4):
            for k in range(-3, 4):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+3, j+3, k+3]
               norm_kernel += mask[i, j, k] * kernel[i+3, j+3, k+3]
    return cumul_kernel/norm_kernel


@nb.stencil(neighborhood = ((-4, 4),(-4, 4)), standard_indexing=("kernel",))
def stencil_kernel9(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-4, 5):
        for j in range(-4, 5):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+4, j+4]
            norm_kernel += mask[i, j] * kernel[i+4, j+4]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-4, 4),(-4, 4),(-4, 4)), standard_indexing=("kernel",))
def stencil_kernel9_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-4, 5):
        for j in range(-4, 5):
            for k in range(-4, 5):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+4, j+4, k+4]
               norm_kernel += mask[i, j, k] * kernel[i+4, j+4, k+4]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-5, 5),(-5, 5)), standard_indexing=("kernel",))
def stencil_kernel11(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-5, 6):
        for j in range(-5, 6):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+5, j+5]
            norm_kernel += mask[i, j] * kernel[i+5, j+5]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-5, 5),(-5, 5),(-5, 5)), standard_indexing=("kernel",))
def stencil_kernel11_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-5, 6):
        for j in range(-5, 6):
            for k in range(-5, 6):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+5, j+5, k+5]
               norm_kernel += mask[i, j, k] * kernel[i+5, j+5, k+5]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-9, 9),(-9, 9)), standard_indexing=("kernel",))
def stencil_kernel19(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-9, 10):
        for j in range(-9, 10):
            cumul_kernel += image[i, j] * mask[i, j] * kernel[i+9, j+9]
            norm_kernel += mask[i, j] * kernel[i+9, j+9]
    return cumul_kernel/norm_kernel

@nb.stencil(neighborhood = ((-9, 9),(-9, 9),(-9, 9)), standard_indexing=("kernel",))
def stencil_kernel19_3d(image, mask, kernel):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    norm_kernel = 1.e-15
    for i in range(-9, 10):
        for j in range(-9, 10):
            for k in range(-9, 10):
               cumul_kernel += image[i, j, k] * mask[i, j, k] * kernel[i+9, j+9, k+9]
               norm_kernel += mask[i, j, k] * kernel[i+9, j+9, k+9]
    return cumul_kernel/norm_kernel


@nb.guvectorize(
    [(nb.float64[:, :], nb.int8[:, :], nb.float64[:, :], nb.float64[:, :])],
    '(m, n), (m, n), (k, k) -> (m, n)', cache=True, fastmath=True,
    nopython=True, target='parallel')
def stencil_kernel_ufunc(data, mask, kernel, filtered_data):
    """


    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.
    filtered_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    if kernel.shape[-1] == 3:
        filtered_data[:] = stencil_kernel3(data, mask, kernel)
    elif kernel.shape[-1] == 5:
        filtered_data[:] = stencil_kernel5(data, mask, kernel)
    elif kernel.shape[-1] == 7:
        filtered_data[:] = stencil_kernel7(data, mask, kernel)
    elif kernel.shape[-1] == 9:
        filtered_data[:] = stencil_kernel9(data, mask, kernel)
    elif kernel.shape[-1] == 11:
        filtered_data[:] = stencil_kernel11(data, mask, kernel)
    else:
        filtered_data[:] = stencil_kernel19(data, mask, kernel)

@nb.guvectorize(
    [(nb.float64[:, :, :], nb.int8[:, :, :], nb.float64[:, :, :], nb.float64[:, :, :])],
    '(l, m, n), (l, m, n), (k, k, k) -> (l, m, n)', cache=True, fastmath=True,
    nopython=True, target='parallel')
def stencil_kernel_3d_ufunc(data, mask, kernel, filtered_data):
    """


    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.
    filtered_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    if kernel.shape[-1] == 3:
        filtered_data[:] = stencil_kernel3_3d(data, mask, kernel)
    elif kernel.shape[-1] == 5:
        filtered_data[:] = stencil_kernel5_3d(data, mask, kernel)
    elif kernel.shape[-1] == 7:
        filtered_data[:] = stencil_kernel7_3d(data, mask, kernel)
    elif kernel.shape[-1] == 9:
        filtered_data[:] = stencil_kernel9_3d(data, mask, kernel)
    elif kernel.shape[-1] == 11:
        filtered_data[:] = stencil_kernel11_3d(data, mask, kernel)
    else:
        filtered_data[:] = stencil_kernel19_3d(data, mask, kernel)


@nb.jit(
        nopython=True, fastmath=True, parallel=True, cache=True)
def filter_image_cube(image_cube, mask_cube, kernel_stack):
    """
    Jitted image cube filter.

    Parameters
    ----------
    image_cube : TYPE
        DESCRIPTION.
    mask_cube : TYPE
        DESCRIPTION.
    kernel_stack : TYPE
        DESCRIPTION.

    Returns
    -------
    fitered_image : TYPE
        DESCRIPTION.

    """
    fitered_image = np.empty(kernel_stack.shape[0:1]+image_cube.shape)
    for k, kernel in enumerate(kernel_stack):
        for image, mask in zip(image_cube, mask_cube):
            if kernel_stack.ndim == 4:
                if kernel.shape[-1] == 3:
                    fitered_image[k, ...] = stencil_kernel3_3d(image, mask, kernel)
                elif kernel.shape[-1] == 5:
                    fitered_image[k, ...] = stencil_kernel5_3d(image, mask, kernel)
                elif kernel.shape[-1] == 7:
                    fitered_image[k, ...] = stencil_kernel7_3d(image, mask, kernel)
                elif kernel.shape[-1] == 9:
                    fitered_image[k, ...] = stencil_kernel9_3d(image, mask, kernel)
                elif kernel.shape[-1] == 11:
                    fitered_image[k, ...] = stencil_kernel11_3d(image, mask, kernel)
                else:
                    fitered_image[k, ...] = stencil_kernel19_3d(image, mask, kernel)
            else:
                if kernel.shape[-1] == 3:
                   fitered_image[k, ...] = stencil_kernel3(image, mask, kernel)
                elif kernel.shape[-1] == 5:
                    fitered_image[k, ...] = stencil_kernel5(image, mask, kernel)
                elif kernel.shape[-1] == 7:
                    fitered_image[k, ...] = stencil_kernel7(image, mask, kernel)
                elif kernel.shape[-1] == 9:
                    fitered_image[k, ...] = stencil_kernel9(image, mask, kernel)
                elif kernel.shape[-1] == 11:
                    fitered_image[k, ...] = stencil_kernel11(image, mask, kernel)
                else:
                    fitered_image[k, ...] = stencil_kernel19(image, mask, kernel)
    return fitered_image


def filter_image_cube_ufunc(image_cube, mask_cube, kernel_stack):
    """
    Image cube filter.

    Parameters
    ----------
    image_cube : TYPE
        DESCRIPTION.
    mask_cube : TYPE
        DESCRIPTION.
    kernel_stack : TYPE
        DESCRIPTION.

    Returns
    -------
    fitered_image : TYPE
        DESCRIPTION.

    """
    if kernel_stack.ndim == 4:
        stencil_ufunc = stencil_kernel_3d_ufunc
    else:
        stencil_ufunc = stencil_kernel_ufunc

    filtered_image = np.empty(kernel_stack.shape[0:1]+image_cube.shape)
    for k, kernel in enumerate(kernel_stack):
        stencil_ufunc(image_cube, mask_cube, kernel, filtered_image[k, ...])
    return filtered_image


@nb.stencil(neighborhood = ((-1, 1),(-1, 1),(-1, 1)))
def stencil_local_maximum(image, mask):
    """
    Numba kernel stencil.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if mask[0, 0, 0] == 0:
        return 0

    max_val = -1.e15
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if (i, j, k) != (0, 0, 0):
                    max_val = max(max_val, image[i, j, k]*mask[i, j, k])

    if image[0, 0, 0] > max_val:
        return 1
    else:
        return 0

@nb.stencil
def stencil_non_max_suppression(image, angle):
    """
    Non max suppression stencil

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    angle : TYPE
        DESCRIPTION.

    Returns
    -------
    value : TYPE
        DESCRIPTION.

    """
    #angle 0
    if (0 <= angle[0, 0] < 22.5) or (157.5 <= angle[0, 0] <= 180):
        q = image[0, 1]
        r = image[0, -1]
    #angle 45
    elif (22.5 <= angle[0,0] < 67.5):
        q = image[-1, -1]
        r = image[1, 1]
    #angle 90
    elif (67.5 <= angle[0,0] < 112.5):
        q = image[1, 0]
        r = image[-1, 0]
    #angle 135
    elif (112.5 <= angle[0,0] < 157.5):
        q = image[1, -1]
        r = image[-1, 1]

    if (image[0,0] >= q) and (image[0,0] >= r):
        return image[0,0]

    return 0.0

@nb.guvectorize(
    [(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :])],
    '(m, n), (m, n) -> (m, n)', cache=True, fastmath=True,
    nopython=True, target='parallel')
def stencil_non_max_suppression_ufunc(data, angle, filtered_data):
    """
    Non max suppression ufunc.

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    angle : TYPE
        DESCRIPTION.
    filtered_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    filtered_data[:] = stencil_non_max_suppression(data, angle)

def non_max_suppression(image_cube, angle_cube):
    """
    Non max suppression filter.

    Parameters
    ----------
    image_cube : TYPE
        DESCRIPTION.
    angle_cube : TYPE
        DESCRIPTION.

    Returns
    -------
    filtered_image_cube : TYPE
        DESCRIPTION.

    """
    filtered_image_cube = np.empty(image_cube.shape)
    stencil_non_max_suppression_ufunc(image_cube, angle_cube, filtered_image_cube)
    return filtered_image_cube

@nb.stencil(neighborhood = ((-1, 1),(-1, 1)), standard_indexing=("kernel",))
def stencil_edge_detection(image, kernel):
    """
    Numba kernel stencil for edge detection.

    Kernel must add up to zero.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    for i in range(-1, 2):
        for j in range(-1, 2):
            cumul_kernel += image[i, j] * kernel[i+1, j+1]
    return cumul_kernel

@nb.stencil(neighborhood = ((-2, 2),(-2, 2)), standard_indexing=("kernel",))
def stencil_edge_detection5(image, kernel):
    """
    Numba kernel stencil for edge detection.

    Kernel must add up to zero.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cumul_kernel = 0.0
    for i in range(-2, 3):
        for j in range(-2, 3):
            cumul_kernel += image[i, j] * kernel[i+2, j+2]
    return cumul_kernel

@nb.guvectorize(
    [(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :])],
    '(m, n), (k, k) -> (m, n)', cache=True, fastmath=True,
    nopython=True, target='parallel')
def stencil_edge_detection_ufunc(data, kernel, filtered_data):
    if kernel.shape[-1] == 3:
        filtered_data[:] = stencil_edge_detection(data, kernel)
    else:
        filtered_data[:] = stencil_edge_detection5(data, kernel)

def filter_image_cube_edge_detection(image_cube, kernel_stack):
    """
    Image cube filter.

    Parameters
    ----------
    image_cube : TYPE
        DESCRIPTION.
    mask_cube : TYPE
        DESCRIPTION.
    kernel_stack : TYPE
        DESCRIPTION.

    Returns
    -------
    fitered_image : TYPE
        DESCRIPTION.

    """
    filtered_image = np.empty(kernel_stack.shape[0:1]+image_cube.shape)
    for k, kernel in enumerate(kernel_stack):
        stencil_edge_detection_ufunc(image_cube, kernel, filtered_image[k, ...])
    return filtered_image

@nb.stencil(neighborhood = ((-1, 1),(-1, 1)))
def stencil_hysteresis(image, weak, strong):
    """
    Numba kernel stencil for edge detection.

    Kernel must add up to zero.

    Parameters
    ----------
    image : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    if image[0, 0] == weak:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if image[i, j] == strong:
                    return strong
        return 0
    return image[0, 0]

@nb.guvectorize(
    [(nb.int32[:, :], nb.int32, nb.int32, nb.int32[:, :])],
    '(m, n), (), () -> (m, n)', cache=True, fastmath=True,
    nopython=True, target='parallel')
def stencil_hysteresis_ufunc(data, weak, strong, filtered_data):
    filtered_data[:] = stencil_hysteresis(data, weak, strong)

def filter_hysteresis(image_cube, weak, strong):
    filtered_image_cube = np.empty(image_cube.shape, dtype=np.int32)
    stencil_hysteresis_ufunc(image_cube, weak, strong, filtered_image_cube)
    return filtered_image_cube