# Understanding H-gamma

This project aims to measure and understand H-gamma and OIII emissions present in Little Red Dots(LRDs). By taking these measurements,
the goal is to figure out what Little Red Dots are. 

The data used for this project is not available to the public.

## Programs

* ratio_histo_calc.py
    This program calculates the ratio of OIII by Hg. It incorporates the redshift of each file and the measurements of each emission 
    taken by LiME to perform the calculation. After taking the measurements and printing them out, it plots a histogram of the data 
    using matplotlib's plt.hist() function.
* Wavelength_calc.py
    This program measures the emissions lines of H-gamma and OIII. Using LiME, it incorporates the redshift for each individual file
    and plots a spectra. The spectra in this program focuses on the OIII emission. It highlights the specific area of the OIII
    emission in yellow.
* single_filter_code.py
  This program does multiple things. However, only some is actually important to the overall project. It plots individual spectra 
  for each of the files. The spectra in this program focuses on the H-gamma emission. It highlights the specific area of the
  H-gamma emission in blue.

## Installation
This project was developed in PyCharm using Python.
NOTE: All the installations were done using the Terminal in Bash (pip)

* LiME (Line Models and Extraction):
    Open your terminal and run:
        pip install lime-stable
    You can quickly verify that LIME is installed by opening a Python script or console and importing it:
        import lime
* astropy:
    Open your terminal and run:
        pip install astropy
* glob2:
    Open your terminal and run:
        pip install glob2
    To verify, you can open a Python script or console and do:
        import glob2 as glob
* matplotlib:
    Open your terminal and run:
        pip install matplotlib
