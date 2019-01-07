# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.units import Quantity
from gammapy.time import random_times
from gammapy.time.running_exptest import running_exptest
import datetime
def test_running_exptest(nb_event):
    rate = Quantity(10, "s^-1")
    time_delta = random_times(10000, rate=rate, return_diff=True, random_state=0)  
    b=datetime.datetime.now()
    mr = running_exptest(time_delta,nb_event)
    print(datetime.datetime.now()-b)
    assert_allclose(mr, 3.058967)
    
test_running_exptest(100)
