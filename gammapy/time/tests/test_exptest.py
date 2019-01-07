# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.units import Quantity
from gammapy.time import random_times, exptest
import datetime
import numpy as np
#from ..exptest import exptest
#from ..simulate import random_times

def test_exptest():
    rate = Quantity(10, "s^-1")
    time_delta = random_times(1000, rate=rate, return_diff=True, random_state=0)
    b=datetime.datetime.now()
    mr = exptest(time_delta)
    print(datetime.datetime.now()-b)
    assert_allclose(mr, 1.379063)
    

test_exptest()
