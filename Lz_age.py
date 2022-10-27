#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:02:24 2022

@author: christian
"""

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from Plotting_scripts import contour_plot, average_line


# Help Message
PROGNAME = sys.argv[0].split('/')[-1]


def helpmessage():
    print('')
    print('The age against the angular momentum (Lz) on an ')
    print('x-y diagram with only metal rich stars. There are ')
    print('running medians through the top and bottom half of ')
    print('the panel to point out the double structure in the ')
    print('diagram.')
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

    metal_rich = feh >= 0.2

    high_Lz = np.logical_and(L_z > 1725, metal_rich)
    low_lz = np.logical_and(L_z <= 1725, metal_rich)

    output = 'Lz_age.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=200)

    fig.text(0.57, 0.015, r'Age [Gyrs]', ha='center', size=18)
    fig.text(0.015, 0.56, r"$L_z$ [km  kpc s$^{-1}$]", va='center',
             rotation='vertical', size=18)

    contour_plot(age[metal_rich], L_z[metal_rich], ax, xlim=[0, 9],
                 ylim=[1001, 2499])
    average_line(age[high_Lz], L_z[high_Lz], ax, 100, median=True,
                 include=0.5, color='blue', xrange=[0.75, 8.1])
    average_line(age[low_lz], L_z[low_lz], ax, 100, median=True,
                 include=0.5, color='blue', xrange=[0.75, 8.1])


    fig.subplots_adjust(left=0.24, right=0.9999, bottom=0.15, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    pdf.close()
