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
    print('The radial and tangential velocity components ')
    print('on an x-y plot with contours to signify the ')
    print('density of stars.')
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
    v_r = np.array([])
    v_t = np.array([])

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
            v_r = np.append(v_r, float(line.split()[18]))
            v_t = np.append(v_t, float(line.split()[19]))

    metal_rich = feh >= 0.2

    high_Lz = np.logical_and(L_z > 1725, metal_rich)
    low_lz = np.logical_and(L_z <= 1725, metal_rich)

    output = 'vR_vT.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=200)

    fig.text(0.57, 0.015, r'$v_r$ [km s$^{-1}$]', ha='center', size=18)
    fig.text(0.015, 0.56, r"$v_t$ [km s$^{-1}$]", va='center',
             rotation='vertical', size=18)

    contour_plot(v_r[metal_rich], v_t[metal_rich], ax, xlim=[-120, 120],
                 ylim=[100, 300])


    fig.subplots_adjust(left=0.24, right=0.9999, bottom=0.15, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    pdf.close()