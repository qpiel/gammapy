# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np

__all__ = ["cusum"]



def cusum(timedelta):
    """Compute the variability for a dataset
    The output is the quantization of the variability as defined in ...
    The output will be 0 for steady sources

    Parameters
    ---------
    timedelta : array-like of time objects
    	Time differences between consecutive events

    Returns
    ------
    signi : float
    	Variability of the dataset

    References
    ----------
    [1]to be updated ...
    """

    somme = 0
    signif_max = 0
    signi = 0
    delta_corrected = (timedelta - np.mean(timedelta))
    somme = np.cumsum(delta_corrected)
    indice = np.array(np.linspace(1,len(delta_corrected),len(delta_corrected)))
    den = np.sqrt(indice*np.power(np.mean(timedelta).value,2)*(1+indice/(float(len(timedelta)))-2*indice/(float(len(timedelta)))))
    mask_0 = den != 0 
    signi= somme[mask_0] /den[mask_0]
    
    return np.max(signi) 
    