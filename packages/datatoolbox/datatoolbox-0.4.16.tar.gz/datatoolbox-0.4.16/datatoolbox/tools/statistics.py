#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:28:02 2020

@author: ageiges
"""


import xarray as xr
import numpy as np
import pandas as pd
#%%

def compute_percentile(data, 
                        perc, 
                        weights=None):
    """
    Fnction to compute the unweighted and weighted percentile for 
    clustered country-level data

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    perc : TYPE
        DESCRIPTION.
    weights : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # un-weighted
    if weights is None:
        mask = ~np.isnan(data)
        data = data[mask]
        result  = np.percentile(data, perc*100)
        return result
    
    
    # weighted
    mask = ~np.isnan(data)
    data = data[mask]
    weights = weights[mask]
    
    
    ix = np.argsort(data)
    
    # Sort data and weights
    sort_data = data[ix]
    sort_weights = weights[ix]
    
    cdf = (np.cumsum(sort_weights) - 0.5 * sort_weights) / np.sum(sort_weights)
    result = np.interp(perc, cdf, sort_data)
    
    return result