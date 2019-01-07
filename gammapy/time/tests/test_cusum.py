# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.units import Quantity
from gammapy.time import random_times
from gammapy.time.cusum import cusum 


def test_cusum():
    rate = Quantity(10, "s^-1")
    time_delta = random_times(10000, rate=rate, return_diff=True, random_state=0) 
    signi = cusum(time_delta)
    assert_allclose(signi.value, 2.251628)
    
test_cusum()