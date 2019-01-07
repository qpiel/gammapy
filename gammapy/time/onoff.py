# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from scipy.special import erfcinv, erfc
from gammapy.stats import significance

__all__ = ["onoff"]



def onoff(deltatime,dT):
    """Compute the variability for a dataset
    The output is the quantization of the variability as defined in ...

    Parameters
    ---------
    time_delta : array-like
        Time differences between consecutive events
    dT : float
        Time to ise for intervals (s)

    Returns
    ------
    signi : float
        Significance of detection

    References
    ----------
    [1] ...
    """
    cumul_deltatime = np.cumsum(deltatime.value)
    event_list = np.asarray([])
    significance_list = np.asarray([])
    for i in range(0,int(np.sum(deltatime).value/dT-1)):
        mask = (cumul_deltatime > float(i)*dT) & (cumul_deltatime < float(i+1)*dT)
        event_list = np.append(event_list,len(cumul_deltatime[mask])) 
    for j in range(0,int(np.sum(deltatime).value/dT-1)):
        significance_list = np.append(significance_list,significance(event_list[j],(np.sum(event_list)-event_list[j])/(len(event_list)-1), method='lima'))
    mask = significance_list < 4.5
    while mask.any() == False:
        for j in range(0,int(np.sum(deltatime).value/dT-1)):
            significance_list[j] = significance(event_list[j],(np.sum(event_list[mask])-event_list[j])/len(event_list[mask]), method='lima')
        mask = mask * significance_list < 4.5

    if np.max(significance_list)>8.3:
        signi_post = erfcinv(erfc(np.max(significance_list)/np.sqrt(2))*float(len(significance_list)))*np.sqrt(2)
    else :
       signi_post = erfcinv(1-np.power(1-erfc(np.max(significance_list)/np.sqrt(2)),float(len(significance_list))))*np.sqrt(2)

    return signi_post

