'''original single_filter_code program. Only draws red line, no units, all fits, no gamma lines, no sigma, no redshift

import astropy.io.fits as fits
import matplotlib.pyplot as plt
from pathlib import Path

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'

fits_files = list(data_folder.glob('*.fits'))
fits_files = fits_files[0:1]

print(f"Found {len(fits_files)} FITS files to plot!\n")


for file_path in fits_files:
    print(f"Processing {file_path.name}")
    # Open the FITS file
    hdul = fits.open(file_path)
    data_layer = hdul[1].data

    print(data_layer)

    wavelength = data_layer['Wavelength']
    flux = data_layer['Flux']

    hdul.close()

    # Make canvas/creat plot
    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, flux, drawstyle='steps-mid', color='crimson', label='LRD Spectrum')
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(f'Spectrum: {file_path.name}')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    output_image_name = f"{file_path.stem}_plot.png"

    # Save the plot
    plt.savefig(output_image_name, dpi=300)

    plt.close()
'''

'''Original FWHM calculations. Unneeded since they were provided

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path

data_folder = Path('data/reextrac2/f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits')

# https://docs.astropy.org/en/stable/io/fits/index.html?__cf_chl_f_tk=0a6flnA62Hm3a7UkBsJWyPMFPxotTvL6uGaFsJY2Wbo-1783001012-1.0.1.1-gXLraO1Oew.ccaW7rBkDzOzQobYJ319ikG5mYqc.OoQ
with fits.open(data_folder) as hdul:
    hdul[1].columns.info()
    table_data = hdul[1].data

flux = table_data['flux']
wavelength = table_data['wavelength']

# https://stackoverflow.com/questions/18689512/efficiently-checking-if-arbitrary-object-is-nan-in-python-numpy-pandas
valid = ~np.isnan(flux) & ~np.isnan(wavelength)
x_all = wavelength[valid]
y_all = flux[valid]

peak_idx_all = np.argmax(y_all)

window = 30

start = max(0, peak_idx_all - window)
end = min(len(y_all), peak_idx_all + window)

x_data = x_all[start:end]
profile = y_all[start:end]

# get half max val
background = np.min(profile)
peak_val = np.max(profile)
half_max = background + (peak_val - background) / 2.0

#https://stackoverflow.com/questions/49100778/fwhm-calculation-using-python
peak_index = np.argmax(profile)
left_side = profile[:peak_index + 1]
right_side = profile[peak_index:]

x_left = x_data[:peak_index + 1]
x_right = x_data[peak_index:]

hm_x_left = np.interp(half_max, left_side, x_left)
hm_x_right = np.interp(half_max, right_side[::-1], x_right[::-1])

# calc FWHM
fwhm = hm_x_right - hm_x_left
fwhm_angstrom = fwhm * 10000

# Plots the graph
plt.figure(figsize=(8, 5))
plt.plot(x_data, profile, 'bo-', label='Spectral Line Profile')
plt.axhline(half_max, color='r', linestyle='--', label=f'Half Max: {half_max:.2e}')

plt.plot([hm_x_left, hm_x_right], [half_max, half_max], 'ro-', label=f'FWHM: {fwhm_angstrom:.4f} (A)')

plt.title('Spectral Line FWHM')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.legend()
plt.show()

output_name =(f"fwhm_graph.png")
plt.savefig(output_name, dpi=300)
'''

