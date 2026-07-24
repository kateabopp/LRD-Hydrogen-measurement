# Generates plot with spectra, H-gamma line and O3 line. Also calculates the lower limit of the flux.

# print(repr(hdul[1].header)) - gets info on fits header - need it for error range

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from pathlib import Path
import astropy.units as u

# 's000001794': (3.681, ), 's000102364': (4.542, ), 's000101393': (3.850, ),     's000101208': (5.682, ),

# fits ID: redshift, sigma value in microns
galaxy_data = {
    's000161695': (5.666, 0.49882810),
    's000020504': (5.276, 1.13207095),
    's000035829': (6.684, 0.94523940),
    's000100424': (4.953, 0.80584327),
    's000033842': (5.287, 1.08391650),
    's000169045': (5.239, 0.89721000)
}

# Constant rest wave for H gamma in microns
rest_wave = 0.43417

# Rest wavelength of [OIII] in microns
rest_wave_o3 = 0.43632

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'
final_folder = current_folder / 'single_filter_plots'/ 'oxy3_hg_plots'

fits_files = list(data_folder.glob('*.fits'))

print(f"Found {len(fits_files)} FITS files to plot!\n")

for file_path in fits_files:

# https://www.codecademy.com/resources/docs/python/built-in-functions/next
    matched_id = next((source_id for source_id in galaxy_data if source_id in file_path.name), None)

# if not found in previous dictionary
    if matched_id is None:
        print(f"Skipping {file_path.name} (Not found in dictionary)")
        print('---')
        continue

    z, sigma = galaxy_data[matched_id]

    h_gamma_obs = rest_wave * (1 + z)
    o3_obs = rest_wave_o3 * (1 + z)

    # Open the FITS file
    hdul = fits.open(file_path)

    data_layer = hdul[1].data
    wavelength = data_layer['Wavelength']
    flux = data_layer['Flux']
    flux_error = data_layer['Flux_Error']
    flux_error_med = np.median(flux_error)

    hdul.close()

    # Make canvas/creat plot
    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, flux, drawstyle='steps-mid', color='crimson', label='LRD Spectrum')

    # add H-gamma
    plt.axvline(x=h_gamma_obs, color='blue', linestyle='--', linewidth=1.5, label=r'H$\gamma$ Line')
    plt.axvline(x=o3_obs, color='gold', linestyle='--', linewidth=1.5, label=r'O3 Line')

    # find sigma range (x-axis, blue shaded area)
    '''wave_min = h_gamma_obs - (0.5 * sigma)
    # print(wave_min)
    wave_max = h_gamma_obs + (0.5 * sigma)
    # print(wave_max)

    # gets range of wavelengths from min to max of blue shaded
    window_mask = (wavelength >= wave_min) & (wavelength <= wave_max)

    line_core_width = 0.005
    clean_noise_mask = window_mask & ((wavelength < (h_gamma_obs - line_core_width)) | (wavelength > (h_gamma_obs + line_core_width)))

    wave_array = wavelength[window_mask]

    # Get the clean noise to ignore the narrow line
    error_array = flux_error[clean_noise_mask]

    D_lambda = np.median(np.diff(wave_array))
    integrated_flux_sigma = D_lambda * np.sqrt(np.sum(error_array ** 2))
    three_sigma_limit = 3 * integrated_flux_sigma

    # shade place between -0.5 sigma and +0.5 sigma
    
    '''#plt.axvspan(wave_min, wave_max, color='blue', alpha=0.15, label=r'Sigma wavelength range')


    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(f'Spectrum: {file_path.name}')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    output_image_name = f"{file_path.stem}_plot.png"

    # Saves the plot
    plt.savefig(final_folder / output_image_name, dpi=300)
    plt.close()
   # print(repr(hdul[1].header))

    #print(f'For fits {output_image_name} | Broad component upper limit is {three_sigma_limit}')
    #print('---')