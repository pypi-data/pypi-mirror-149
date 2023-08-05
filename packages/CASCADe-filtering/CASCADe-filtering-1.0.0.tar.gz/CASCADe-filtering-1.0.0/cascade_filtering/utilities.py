#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:03:54 2022

@author: bouwman
"""

import numpy as np
import os
import fnmatch

__all__=['create_mask_from_dq', 'find']

def find(pattern, path):
    """
    Return  a list of all data files.

    Parameters
    ----------
    pattern : 'str'
        Pattern used to search for files.
    path : 'str'
        Path to directory to be searched.

    Returns
    -------
    result : 'list' of 'str'
        Sorted list of filenames matching the 'pattern' search
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return sorted(result)


def create_mask_from_dq(dq_cube, bits_not_to_flag=[]):
    """
    Create mask from DQ cube.

    Parameters
    ----------
    dq_cube : TYPE
        DESCRIPTION.

    Returns
    -------
    mask : TYPE
        DESCRIPTION.

    Note
    ----
    Standard bit values not to flag are 0, 12 and 14.
    Bit valiue 10 (blobs) is not set by default but can be selected not to
    be flagged in case of problem.
    """
    bits_not_to_flag = bits_not_to_flag
    bits_to_flag = []
    for ibit in range(1, 16):
        if ibit not in bits_not_to_flag:
            bits_to_flag.append(ibit)
    all_flag_values = np.unique(dq_cube)
    bit_select = np.zeros_like(all_flag_values, dtype='int')
    for ibit in bits_to_flag:
        bit_select = bit_select + (all_flag_values & (1 << (ibit - 1)))
    bit_select = bit_select.astype('bool')
    mask = np.zeros_like(dq_cube, dtype='bool')
    for iflag in all_flag_values[bit_select]:
        mask = mask | (dq_cube == iflag)
    return mask