# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import matplotlib.pyplot as plt
from gammapy.time.exptest import exptest


def initialise_transient_RTA_map(target_ra,target_dec):
    #To be ran at the run beginning
    binsize = 0.1 #deg
    fov = 5. #deg

    ra_bin, dec_bin, event_bin = create_RTA_Map(binsize,target_ra,target_dec,fov)
    signi = np.zeros((len(ra_bin),len(dec_bin)))
    plot_transient_RTA_map(ra_bin,dec_bin,binsize,signi)

def update_transient_RTA_map(event_list, ra_bin,dec_bin, event_bin, signi_bin):
    

    for i in range(0,len(event_list)):
        index_ra = np.argmin(np.absolute(ra_bin-event_list[i].ra))
        index_dec = np.argmin(np.absolute(dec_bin-event_list[i].dec))
        event_bin[index_ra[i]][index_dec] = np.append(event_bin[index_ra[i]][index_dec],event_list.time[i])
        delta_time = event_bin[index_ra[i]*][index_dec][1:]-event_bin[index_ra[i]][index_dec][:-1] #a verifier
        signi = exptest(delta_time)
        signi_bin[index_ra[i]][index_dec[i]] = signi
    plot_transient_RTA_map(ra_bin,dec_bin,signi_bin)

