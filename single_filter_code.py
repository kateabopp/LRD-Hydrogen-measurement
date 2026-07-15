# print(repr(hdul[1].header)) - gets info on fits header - need it for error range

# find units - done
# add h gamma line using observed wave - done
# Add lines from sigma - done
# Find flux error from files - done
# Range of wave is half sigma to half sigma
# Write summary of what I did in part 1 and 2 - done
# Find lower limits
# get wavelength array - done
# get error array - done

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from pathlib import Path

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

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'
final_folder = current_folder / 'single_filter_plots'/ 'single_gamma'

fits_files = list(data_folder.glob('*.fits'))

print(f"Found {len(fits_files)} FITS files to plot!\n")

for file_path in fits_files:
    print(f"Processing {file_path.name}")

# https://www.codecademy.com/resources/docs/python/built-in-functions/next
    matched_id = next((source_id for source_id in galaxy_data if source_id in file_path.name), None)

# if not found in previous dictionary
    if matched_id is None:
        print(f"Skipping {file_path.name} (Not found in dictionary)")
        print('---')
        continue

    z, sigma = galaxy_data[matched_id]

    h_gamma_obs = rest_wave * (1 + z)

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

    # find sigma range (x-axis, blue shaded area)
    wave_min = h_gamma_obs - (0.5 * sigma)
    # print(wave_min)
    wave_max = h_gamma_obs + (0.5 * sigma)
    # print(wave_max)

    # gets range of wavelengths from min to max of blue shaded
    window_mask = (wavelength >= wave_min) & (wavelength <= wave_max)

    wave_array = wavelength[window_mask]
    error_array = flux_error[window_mask]

    D_lambda = np.median(np.diff(wave_array))
    integrated_flux_sigma = D_lambda * np.sqrt(np.sum(error_array ** 2))
    Three_sigma_limit = 3 * integrated_flux_sigma


    # shade place between -0.5 sigma and +0.5 sigm
    plt.axvspan(wave_min, wave_max, color='blue', alpha=0.15, label=r'Sigma wavelength range')

    plt.xlabel('Wavelength (Microns)')
    plt.ylabel('Flux (Janskys)')
    plt.title(f'Spectrum: {file_path.name}')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    output_image_name = f"{file_path.stem}_plot.png"

    # Save the plot
    plt.savefig(final_folder / output_image_name, dpi=300)
    plt.close()
   # print(repr(hdul[1].header))

    print(f'For fits {output_image_name} | Lower flux limit is {integrated_flux_sigma} Janskys')
    print('---')