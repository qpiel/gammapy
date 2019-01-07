# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.units import Quantity
from gammapy.time import random_times
from gammapy.time.onoff import onoff

def test_onoff(dT):
    rate = Quantity(10, "s^-1")
    time_delta = random_times(100, rate=rate, return_diff=True, random_state=0)
    signi = onoff(time_delta,dT)
    assert_allclose(signi, 0.03324258256522262)
    print(mr)

test_onoff(1)
