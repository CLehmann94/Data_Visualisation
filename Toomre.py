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

from Plotting_scripts import contour_plot


# Help Message
PROGNAME = sys.argv[0].split('/')[-1]


def helpmessage():
    print('')
    print('A Toomre digram (tangential velocity component ')
    print('on the x-axis against the combined non-tangential ')
    print('velocity components on the y-axis). The diagram is ')
    print('split into four panels, each displaying a different ')
    print('metallicity range of stars.')
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
    v_t = np.array([])
    v_r = np.array([])
    v_z = np.array([])


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
            v_t = np.append(v_t, float(line.split()[19]))
            v_r = np.append(v_r, float(line.split()[18]))
            v_z = np.append(v_z, float(line.split()[20]))

    v_nt = np.sqrt(np.square(v_r) + np.square(v_z))
    v_ts = v_t - 220

    metal_rich = feh >= 0.3
    metal_solar1 = np.logical_and(feh >= -0.3, feh < 0.3)
    metal_solar2 = np.logical_and(feh >= -0.7, feh < -0.3)
    metal_poor = feh < -0.7

    output = 'Toomre.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(output)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,
                                                 figsize=(6, 6))

    fig.text(0.57, 0.01, r'$v_T - v_{T, \odot}$[km/s]', ha='center',
             size=22)
    fig.text(0.01, 0.56, r"$\sqrt{v_R^2+v_z^2}$[km/s]", va='center',
             rotation='vertical', size=22)

    contour_plot(v_ts[metal_rich], v_nt[metal_rich], ax1, xlim=[-149, 99],
                 ylim=[0, 199], x_notags=True)
    contour_plot(v_ts[metal_solar1], v_nt[metal_solar1], ax2, xlim=[-149, 99],
                 ylim=[0, 199], x_notags=True, y_notags=True)
    contour_plot(v_ts[metal_solar2], v_nt[metal_solar2], ax3, xlim=[-149, 99],
                 ylim=[0, 199])
    contour_plot(v_ts[metal_poor], v_nt[metal_poor], ax4, xlim=[-149, 99],
                 ylim=[0, 199], y_notags=True)

    fig.subplots_adjust(left=0.14, right=0.9999, bottom=0.12, top=0.9999,
                        wspace=0.0, hspace=0.0)

    pdf.savefig(fig)
    pdf.close()
