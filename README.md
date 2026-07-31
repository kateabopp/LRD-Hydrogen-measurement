# Understanding H-gamma and OIII

This project aims to measure and understand H-gamma and OIII emissions present in Little Red Dots(LRDs).
The goal is to figure out what Little Red Dots are by taking these measurements. 

> **_NOTE:_** The data used for this project is not available to the public.

## Scripts

### ratio_histo_calc.py
  This program calculates the ratio of OIII by Hg. It incorporates the redshift of each file and the measurements of each emission 
  taken by LiME to perform the calculation. After taking the measurements and printing them out, it plots a histogram of the data 
  using matplotlib's plt.hist() function. It also includes the error uncertainty calculations and plots them on the final histogram.
### Wavelength_calc.py
  This program measures the emissions lines of H-gamma and OIII. Using LiME, it incorporates the redshift for each individual file
  and plots a spectra. Note that the most of the measurements for H-gamma and OIII are far from accurate as the emission is too broad for LiME to accurately
  calculate.
### single_filter_code.py
  This program does multiple things. However, only some is actually important to the overall project. It plots individual spectra 
  for each of the files. The spectra in this program focuses on both the H-gamma and OIII emission. It highlights the specific area of the
  H-gamma emission in blue and the OIII emission in yellow.
### alpha_ratio.py
  This program plots the ratio of the H-alpha narrow and broad measurements found in https://arxiv.org/pdf/2606.00258. 
  This plot is used to indentify and show two outlier LRDs as they are much farther away from the majority sample.

## Installation
This project was developed in the Community Edition of PyCharm using Python.
> **_NOTE:_** All the installations were done using the Terminal in Bash (pip)

* `Python3`:
  Open your terminal and run:
    ```shell
    sudo apt update
    sudo apt install python3 python3-pip
    ```
    To verify:
    ```shell
    python3 --version
    ```
    To use in PyCharm:
    1. Open PyCharm and go to Settings (or Preferences on Mac) → Project → Python Interpreter
    2. Click Add Interpreter → Add Local Interpreter...
    3. Select System Interpreter (or set up a new Virtualenv)
    4. Select the newly installed Python executable path and click OK

* `Virtual Environment (venv)`:
  Open your terminal and run:
  ```shell
  cd path/to/your/project
  ```
  This moves into your project directory
  ```shell
  python3 -m venv venv
  ```
  (Note: If you get an error on Ubuntu/Debian like No module named venv, install it first via system terminal: sudo apt install python3-venv)
  
  To activate:
  ```shell
  source venv/bin/activate
  ```
* `LiME (Line Models and Extraction)`:
    Open your terminal and run:
    ```shell
    pip install lime-stable
    ```
    You can quickly verify that LIME is installed by opening a Python script or console and importing it:
    ```shell
    import lime
    ```
  
* `astropy`:
    Open your terminal and run:
    ```shell
    pip install astropy
    ```

* `glob2`:
    Open your terminal and run:
    ```shell
    pip install glob2
    ```
    To verify, you can open a Python script or console and do:
    ```shell
    import glob2 as glob
    ```

* `matplotlib`:
    Open your terminal and run:
    ```shell
    pip install matplotlib
    ```

## Producing Results
> **_NOTE:_** Since this project relies on private data unavailable to the public, accurate results will not be reproductable

The results produced by this project (with the proper data) are in the form of plots. To generate these plots, user must have matplotlibs
installed with proper syntax knowledge. To create the final plot (the histogram), you have to collect the data from the following
scripts:
* Wavelength_calc.py: Measures each line emission and collects data for the ratio
* ratio_histo_calc.py: Plots the final histogram (the main result). Includes, redshift, error bars, and shaded regions
* alpha_ratio.py: Plots relationship of narrow to broad measurements of H-alpha emission. Doesn't require specific data 
  to run.
* single_filter_code.py: Plots jagged red spectra of the sources. Highlights the emissions.
* To generate the documents
  ```shell
  sudo apt update && sudo apt install texlive-full
  
  pdflatex docs/KateBopp_GammaOII_slides.tex

  pdflatex docs/KateBopp_GammaOII_report.tex 
  ```

## Data
The 1D extractions used in this work are courtesy of the OCEANS collaboration. The OCEANS program (program ID 8410, PI Raymond Simons)
is publicly accessible on the MAST database. The extractions used in this work will be made available in the coming months. 
For a full description of the reductions used in this work, see Davis 2026 (https://arxiv.org/pdf/2502.03519, https://arxiv.org/pdf/2606.00258)