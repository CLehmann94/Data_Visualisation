#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:32:09 2022

@author: christian
"""

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import numpy as np
import seaborn as sns


def contour_plot(x_data, y_data, ax, xlim=[], ylim=[], xlabel="", ylabel="",
                 xlog=False, ylog=False, legend_loc="", x_notags=False,
                 y_notags=False):
    """Make a contour plot using an array of x and y data. Projected on plt
    object oriented axis (ax)
    Parameters
    ----------
        x_data : array like
            The data for the x-axis.
        y_data : array like
            The data for the x-axis.
        x_lim : array like
            An array with two components setting the limits on the x axis
        y_lim : array like
            An array with two components setting the limits on the y axis
        xlabel : string
            A string labeling the x axis
        ylabel : string
            A string labeling the y axis
        xlog : boolean
            Activate/deactivate logscale on x axis
        ylog : boolean
            Activate/deactivate logscale on y axis
        legend_loc : string
             Activate the legend on the plot by giving it a location (e.g.
             "upper right" or "lower left")
        x_notags : Boolean
            Deactivate tick labels on the x axis
        y_notags : Boolean
            Deactivate tick labels on the y axis

    Returns
    -------
        Nothing, just workd on plot and returns 0

    """
    ax.scatter(x_data, y_data, color="red", s=0.5, alpha=0.1, rasterized=True)
    sns.kdeplot(x_data, y_data, ax=ax)
    if len(xlim) == 2:
        ax.set_xlim(xlim[0], xlim[1])
    else:
        ax.set_xlim(np.min(x_data), np.max(x_data))

    if len(ylim) == 2:
        ax.set_ylim(ylim[0], ylim[1])
    else:
        ax.set_ylim(np.min(y_data), np.max(y_data))

    if xlog is True:
        ax.set_xscale("log")
    if ylog is True:
        ax.set_yscale("log")

    if not legend_loc == "":
        ax.legend(loc="upper left")
    if x_notags is True:
        ax.set_xticklabels([])
    if y_notags is True:
        ax.set_yticklabels([])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_rasterization_zorder(-10)

    return 0


def histogram_plot(x_data, ax, xlim=[], ylim=[], xlabel="", ylabel="",
                   xlog=False, ylog=False, legend_loc="", x_notags=False,
                   y_notags=False, err_point=False, normalise=False,
                   legend_handle=""):
    """Make a contour plot using an array of x and y data. Projected on plt
    object oriented axis (ax)
    Parameters
    ----------
        x_data : array like
            The data for the x-axis.
        x_lim : array like
            An array with two components setting the limits on the x axis
        y_lim : array like
            An array with two components setting the limits on the y axis
        xlabel : string
            A string labeling the x axis
        ylabel : string
            A string labeling the y axis
        xlog : boolean
            Activate/deactivate logscale on x axis
        ylog : boolean
            Activate/deactivate logscale on y axis
        legend_loc : string
             Activate the legend on the plot by giving it a location (e.g.
             "upper right" or "lower left")
        x_notags : Boolean
            Deactivate tick labels on the x axis
        y_notags : Boolean
            Deactivate tick labels on the y axis
        err_point : Boolean
            Activate ploting of points with errorbars
        normalise : Boolean
            Normalise the histogram

    Returns
    -------
        Nothing, just worked on plot and returns 0

    """
    if len(xlim) == 2:
        bins = np.linspace(xlim[0], xlim[1], 20)
    else:
        bins = np.linspace(np.min(x_data), np.max(x_data), 20)

    n, x, _ = ax.hist(x_data, bins=bins, color="white")
    bin_plot, n_plot = 0.5*(x[1:]+x[:-1]), n
    n_plot_err = np.sqrt(n)

    if normalise is True:
        n_plot_err = n_plot_err / sum(n_plot)
        n_plot = n_plot / sum(n_plot)

    if err_point is True:
        ax.errorbar(bin_plot, n_plot, yerr=n_plot_err, ls='none', fmt='o',
                    label=legend_handle)
    else:
        ax.plot(bin_plot, n_plot, label=legend_handle)

    if len(xlim) == 2:
        ax.set_xlim(xlim[0], xlim[1])
    else:
        ax.set_xlim(np.min(x_data), np.max(x_data))

    if len(ylim) == 2:
        ax.set_ylim(ylim[0], ylim[1])
    else:
        ax.set_ylim(np.min(n_plot), np.max(n_plot))

    if xlog is True:
        ax.set_xscale("log")
    if ylog is True:
        ax.set_yscale("log")

    if not legend_loc == "":
        ax.legend(loc="upper left", fontsize=15)
    if x_notags is True:
        ax.set_xticklabels([])
    if y_notags is True:
        ax.set_yticklabels([])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_rasterization_zorder(-10)

    return 0


def average_line(x, y, ax, n_steps, step_range=0, median=False, xrange=[],
                 include=0, color='red'):
    """Plots the running average of a x, y plot
    Parameters
    ----------
        x : array like
            The data for the x-axis.
        y : array like
            The data for the y-axis.


    Returns
    -------
        Nothing, just worked on plot and returns 0

    """
    if len(xrange) == 0:
        xrange = [np.min(x), np.max(x)]
    if step_range == 0:
        step_range = (xrange[1] - xrange[0]) / n_steps
    else:
        n_steps = np.ceil((xrange[1] - xrange[0]) / n_steps)
    if include == 0:
        include = step_range

    average_x = np.array([])
    average_y = np.array([])

    for i in range(n_steps):
        rangeleft = xrange[0] + i * step_range
        av_y = np.array([])

        for x_val, y_val in zip(x, y):
            if x_val >= rangeleft and x_val < rangeleft + include:
                av_y = np.append(av_y, y_val)
        if len(av_y) > 0:
            if median is True:
                average_x = np.append(average_x, rangeleft + include / 2)
                average_y = np.append(average_y, np.median(av_y))
            else:
                average_x = np.append(average_x, rangeleft + include / 2)
                average_y = np.append(average_y, np.average(av_y))

    ax.plot(average_x, average_y, c=color)

    return 0

