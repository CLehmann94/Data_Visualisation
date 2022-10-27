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
    print('An age histogram for stars. It displays both the')
    print('whole set of stars as well as only metal rich ')
    print('stars ([Fe/H] > 0.2).')
    print('')
    print('Usage: ', PROGNAME, '(Options) [.ascii table]')
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
    R_peri = np.array([])

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
            R_peri = np.append(R_peri, float(line.split()[23]))

    middle_metal = feh > 0.2

    young = np.logical_and(age <= 4, middle_metal)
    medium = np.logical_and(np.logical_and(age > 4, age <= 8), middle_metal)
    old = np.logical_and(age > 8, middle_metal)

    metal_rich = feh > 0.2
    solar_metal = np.logical_and(feh > -0.2, feh < 0.2)
    metal_poor = feh < -0.2

    output = 'Age_hist.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(6, 3))

    histogram_plot(age, ax1, xlim=[0.001, 12.999], ylim=[-0.01, 0.199],
                   legend_handle="All solar", normalise=True)
    histogram_plot(age[metal_rich], ax1, xlim=[0.001, 12.999],
                   ylim=[-0.01, 0.199], legend_handle="[Fe/H]>0.2",
                   normalise=True, legend_loc="upper left",
                   xlabel="Age [Gyrs]", ylabel="Norm. count")

    fig.subplots_adjust(left=0.14, right=0.9999, bottom=0.22, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    plt.clf()
    pdf.close()
