import numpy as np
from scipy.special import erfcinv, erfc


def running_exptest(deltatime,nb_event):
        """Compute the variability for a given dataset.
        The dataset is slip into several parts given by nb_event. Exptest is applied on all the sub datasets.
        The ouput is the maximum of the exptest applied to sliding windows. As in the exptest case, the value should be 0 for steady source.

        Parameters
        ---------
        deltatime : array-like of time objects
        	Time differences between consecutive events
        nb_event : int 
            Number of events to apply exptest on

        Returns
        -------
        max_exp_test_post : float
        	Level of variability

    	References
    	----------
        [1] to be updated ...
        """
        
        exp_test_values = []
        nbinterval = np.sum(deltatime).value/nb_event
        if nbinterval < 1:
            print("\033[31m {}\033[00m" .format("dT is higher than the run duration !!! Please change the value."))
        sliding_window = rolling_window(deltatime.value,nb_event,1)

        for i in range(0,len(sliding_window)):
            exp_test_values.append(exptest_modified(sliding_window[i],np.mean(deltatime.value)))
        max_exp_test_post = erfcinv(1-np.power(1-erfc(np.max(exp_test_values)/np.sqrt(2)),(len(exp_test_values) - nb_event)))*np.sqrt(2)
        return max_exp_test_post

def rolling_window(a, window, step_size):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1 - step_size, window)
    strides = a.strides + (a.strides[-1] * step_size,)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def exptest_modified(time_delta,mean_delta_time_total):
    """
    Almost the same Exptest as the function in exptest.py. But the mean value has to be for all the datasample not only the 
    probed one. So a new argument has be used (mean_delta_time_total). See exptest.py for more explanations.
    """

    normalized_time_delta = time_delta / mean_delta_time_total
    mask = normalized_time_delta < 1
    sum_time = 1 - normalized_time_delta[mask] / 1
    sum_time_all = np.sum([sum_time])
    m_value = sum_time_all / len(time_delta)
    term1 = m_value - (1 / 2.71828 - 0.189 / len(time_delta))
    term2 = 0.2427 / np.sqrt(len(time_delta))
    mr = term1 / term2
    return mr
