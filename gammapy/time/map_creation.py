# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import matplotlib.pyplot as plt



def create_RTA_Map(binsize,target_ra,target_dec,fov):
    ra_bin = np.linspace(target_ra-fov,target_ra+fov,2.*fov/binsize)
    dec_bin = np.linspace(target_dec-fov,target_dec+fov,2.*fov/binsize)
    event_bin = np.array(len(ra_bin)*len(dec_bin))
    return ra_bin,dec_bin, event_bin

def plot_transient_RTA_map(ra_bin,dec_bin,binsize,significance):
    X, Y = np.meshgrid(ra_bin, dec_bin)
    extent = np.min(dec_bin), np.max(dec_bin), np.min(ra_bin), np.max(ra_bin)
    plt.imshow(signi,origin='low',interpolation='nearest',aspect='auto',cmap='hot',extent=extent)
    plt.xlabel('RA [deg]')
    plt.ylabel('Dec [deg]')
    plt.title("Significance Map (Exptest)")
    src = plt.colorbar()
    src.set_label('Significance of detection [$\sigma$]')
    plt.show()

def save_previous_data(ra_bin,dec_bin,events):
    np.savetxt('data.txt',ra_bin,dec_bin,events)


