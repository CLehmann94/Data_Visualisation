|Python| |GitHub| 

Data Visualisation Python scripts
=================================
A collection of data visualisation sripts written in Python towards the end of my PhD. They are focused on visualising the age, metallicity and kinematic components of stars with a focus on metal rich solar analogues. 


Usage
=====
The usage is quite simple and designed to be expanded at any time. Scripts that produce contour plots, histograms and other diagrams are saved in "Plotting_scripts.py" so that they can be called by any of the subsequent scripts (e.g. Age_hist.py to make an age histogram) to visualise a table of data (see "example_data/example_table.ascii").

Example use
-----------
Within a Python 3.7 (or upwards) environment with the dependencies installed (see below), a simple function call executes the script, e.g.::

  $ python3 Age_hist.py ./example_data/example_table.ascii

Scripts
-------
Age_hist.py     -> An age histogram for stars. It displays both the whole set of stars as well as only metal rich stars ([Fe/H] > 0.2).

Lz_age.py       -> The age against the angular momentum (Lz) on an x-y diagram with only metal rich stars. There are running medians through the top and bottom half of the panel to point out the double structure in the diagram.

Lz_feh.py       -> The metallicity against the angular momentum (Lz) on an x-y diagram with 4 panels. Each panel has running medians through the top and bottom half of the panels. The panels are displaying sets of stars at different age; top left: 0-4 Gyrs, top right: 4-8 Gyrs, bottom right: 8-12 Gyrs, bottom right: all ages.

Lz_hist.py      -> A histogram of angular momentum of stars within the Milky Way. The top panel shows these histrograms by metallicity and the bottom panel (metal rich stars only) splits by stellar age.

R_peri_hist.py  -> A histogram of perihelion radii of stars within the Milky Way. The top panel shows these histrograms by metallicity and the bottom panel (metal rich stars only) splits by stellar age.

Toomre.py       -> A Toomre digram (tangential velocity component on the x-axis against the combined non-tangential velocity components on the y-axis). The diagram is split into four panels, each displaying a different metallicity range of stars.

vR_vT.py        -> The radial and tangential velocity components on an x-y plot with contours to signify the density of stars.


Dependencies
============
matplotlib, numpy, os, seaborn, sys
