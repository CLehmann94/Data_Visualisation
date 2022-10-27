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
    print('The metallicity against the angular momentum (Lz) ')
    print('on an x-y diagram with 4 panels. Each panel has ')
    print('running medians through the top and bottom half ')
    print('of the panels. The panels are displaying sets of ')
    print('stars at different age; top left: 0-4 Gyrs, ')
    print('top right: 4-8 Gyrs, bottom right: 8-12 Gyrs, ')
    print('bottom right: all ages.')
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

    young = age <= 4
    medium = np.logical_and(age > 4, age <= 8)
    old = age > 8

    high_Lz = L_z > 1700
    low_Lz = L_z <= 1800

    y_high_Lz = np.logical_and(high_Lz, young)
    m_high_Lz = np.logical_and(high_Lz, medium)
    o_high_Lz = np.logical_and(high_Lz, old)
    y_low_Lz = np.logical_and(low_Lz, young)
    m_low_Lz = np.logical_and(low_Lz, medium)
    o_low_Lz = np.logical_and(low_Lz, old)

    output = 'Lz_feh.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,
                                                 figsize=(6, 6), dpi=200)

    fig.text(0.57, 0.01, r'[Fe/H] [dex]', ha='center',
             size=22)
    fig.text(0.01, 0.56, r"$L_z$ [km kpc $^{-1}$]", va='center',
             rotation='vertical', size=22)

    contour_plot(feh[young], L_z[young], ax1, xlim=[-0.099, 0.55],
                 ylim=[1000, 2499], x_notags=True)
    contour_plot(feh[medium], L_z[medium], ax2, xlim=[-0.099, 0.55],
                 ylim=[1000, 2499], x_notags=True, y_notags=True)
    contour_plot(feh[old], L_z[old], ax3, xlim=[-0.099, 0.55],
                 ylim=[1000, 2499])
    contour_plot(feh, L_z, ax4, xlim=[-0.099, 0.55],
                 ylim=[1000, 2499], y_notags=True)

    average_line(feh[y_high_Lz], L_z[y_high_Lz], ax1, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])
    average_line(feh[y_low_Lz], L_z[y_low_Lz], ax1, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])
    average_line(feh[m_high_Lz], L_z[m_high_Lz], ax2, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])
    average_line(feh[m_low_Lz], L_z[m_low_Lz], ax2, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])
    average_line(feh[o_high_Lz], L_z[o_high_Lz], ax3, 35, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.25])
    average_line(feh[o_low_Lz], L_z[o_low_Lz], ax3, 35, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.25])
    average_line(feh[high_Lz], L_z[high_Lz], ax4, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])
    average_line(feh[low_Lz], L_z[low_Lz], ax4, 50, median=True,
                 include=0.05, color='blue', xrange=[-0.099, 0.41])

    fig.subplots_adjust(left=0.14, right=0.9999, bottom=0.12, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    pdf.close()