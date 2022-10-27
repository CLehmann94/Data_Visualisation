#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:10:56 2022

@author: christian
"""

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from Plotting_scripts import histogram_plot


# Help Message
PROGNAME = sys.argv[0].split('/')[-1]


def helpmessage():
    print('')
    print('A histogram of angular momentum of stars within ')
    print('the Milky Way. The top panel shows these histrograms ')
    print('by metallicity and the bottom panel (metal rich ')
    print('stars only) splits by stellar age.')
    print('')
    print('Usage: ', PROGNAME, '(Options) [EW.dat]')
    print('')
    print('Options:  -help              Print this message.')
    print('')
    sys.exit(3)


if __name__ == '__main__':
    argc = len(sys.argv)
    ref_name = sys.argv[-1]

    feh = np.array([])
    L_z = np.array([])
    age = np.array([])

# looking for help?
    if argc <= 1:
        helpmessage()
    else:
        for i in range(argc):
            if sys.argv[i] == '-help':
                helpmessage()

    with open(ref_name) as stel_param:
        lines = stel_param.readlines()

        for i, line in enumerate(lines):
            if line.startswith(';') or line.startswith('#'):
                continue
            if '""' in line.split():
                continue
            feh = np.append(feh, float(line.split()[8]))
            L_z = np.append(L_z, float(line.split()[21]))
            age = np.append(age, float(line.split()[2]))

    middle_metal = feh > 0.2

    young = np.logical_and(age <= 4, middle_metal)
    medium = np.logical_and(np.logical_and(age > 4, age <= 8), middle_metal)
    old = np.logical_and(age > 8, middle_metal)

    metal_rich = feh > 0.2
    solar_metal = np.logical_and(feh > -0.2, feh < 0.2)
    metal_poor = feh < -0.2

    output = 'Lz_hist.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 9))

    histogram_plot(L_z[metal_rich], ax1, xlim=[1001, 2499], x_notags=True,
                   legend_handle="[Fe/H]>0.3", normalise=True)
    histogram_plot(L_z[solar_metal], ax1, xlim=[1001, 2499], x_notags=True,
                   legend_handle="-0.3<[Fe/H]<0.3", normalise=True)
    histogram_plot(L_z[metal_poor], ax1, xlim=[1001, 2499],
                   ylim=[-0.01, 0.1999], x_notags=True,
                   ylabel="Norm. distribution", legend_handle="[Fe/H]<-0.3",
                   normalise=True, legend_loc="upper right")

    histogram_plot(L_z[young], ax2, xlim=[1001, 2499],
                   legend_handle="age<4Gyrs", normalise=True)
    histogram_plot(L_z[medium], ax2, xlim=[1001, 2499],
                   legend_handle="4Gyrs<age<8Gyrs", normalise=True)
    histogram_plot(L_z[old], ax2, xlim=[1001, 2499], ylim=[-0.01, 0.1999],
                   ylabel="Norm. distribution",
                   xlabel=r"$L_z$ [km kpc $^{-1}$]",
                   legend_handle="age>8Gyrs", normalise=True,
                   legend_loc="upper right")

    fig.subplots_adjust(left=0.14, right=0.9999, bottom=0.09, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    plt.clf()
    pdf.close()
