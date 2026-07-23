# This program generates a sample data file to use while the real data is still private

import os
import numpy as np
from astropy.io import fits

# generates the data
wavelengths = np.linspace(400, 700, 1000)
continuum = 100 / (wavelengths / 400)**2
h_beta_peak = 15 * np.exp(-((wavelengths - 486.1) / 2)**2)
h_alpha_peak = 65 * np.exp(-((wavelengths - 656.3) / 2)**2)
noise = np.random.normal(0, 2, size=len(wavelengths))

flux = continuum + h_beta_peak + h_alpha_peak + noise

# Creates FITS column objects with names and data types
col_wave = fits.Column(name='WAVELENGTH', format='E', unit='nm', array=wavelengths)
col_flux = fits.Column(name='FLUX', format='E', unit='uJy', array=flux)

# Combines the columns
fits_table = fits.BinTableHDU.from_columns([col_wave, col_flux])


# Adds header data
fits_table.header['TELESCOP'] = ('JWST', 'Name of the telescope')
fits_table.header['INSTRUME'] = ('NIRSpec', 'JWST Instrument used')
fits_table.header['TARGET']   = ('CEERS-GALAXY-101', 'Target object identifier')
fits_table.header['PROGRAM']  = ('OCEANS', 'JWST Observing Program')
fits_table.header['AUTHOR']   = ('Intern Pipeline', 'Created by python simulation script')


# saves to data file
os.makedirs('data', exist_ok=True)
output_path = 'data/sample_jwst_galaxy.fits'

# Writes out the FITS file
fits_table.writeto(output_path, overwrite=True)

print(f"Successfully made FITS file: {output_path}")