# Plots spectra with emission highlighted - measures H-gamma and OIII

import numpy as np
from astropy.io import fits
import glob2 as glob
import lime
import matplotlib.pyplot as plt
import astropy.units as u


data_folder = 'data/reextrac2/'
output_folder = 'data/wavelength_results'

redshifts = {
    's000001794': 3.681,
    's000161695': 5.666,
    's000020504': 5.276,
    's000035829': 6.684,
    's000102364': 4.542,
    's000100424': 4.953,
    's000101393': 3.850,
    's000101208': 5.682,
    's000033842': 5.287,
    's000169045': 5.239
}

for file_address in glob.glob(data_folder + '*.fits'):
    print(file_address)
    # file_address = 'data/reextrac2/f170lp_g235h_s000020504_x1d_nodded-bg_P1_errescaled.fits'

    z_val = redshifts[file_address.split('_')[2]]

    hdul = fits.open(file_address)
    wavelength_microns = hdul[1].data['Wavelength']
    flux_array = hdul[1].data['Flux']
    hdul.close()

    # https://lime-stable.readthedocs.io/en/latest/1_introduction/4_lines_database.html
    spec = lime.Spectrum.from_file(file_address, instrument='nirspec', redshift=z_val)

    spec.unit_conversion(wave_units_out='Angstrom', flux_units_out=u.erg/u.s/(u.cm**2))

    spec.fit.bands('H1_4340A', cont_source='adjacent')
    spec.fit.bands('O3_4363A', cont_source='adjacent')

    try:
        profile_flux_gamma = spec.frame.loc[['H1_4340A'], ['profile_flux']].iloc[0, 0]
        profile_flux_oxy = spec.frame.loc[['O3_4363A'], ['profile_flux']].iloc[0, 0]

    except Exception as e:
        print(e)


    spec.plot.bands(rest_frame=True, show_cont=False)

    rest_wave_o3 = 0.43632  # Rest wavelength of [OIII] in microns
    o3_obs = rest_wave_o3 * (1 + z_val)

    # Create canvas
    plt.figure(figsize=(10, 5))

    plt.plot(wavelength_microns, flux_array, drawstyle='steps-mid', color='crimson', label='LRD Spectrum')

    # Highlight [OIII] in the observed frame
    plt.axvline(x=o3_obs, color='gold', linestyle='--', linewidth=2, label='[OIII] Line')

    output_name = file_address.split('_')[2]
    plt.title(f'Spectrum: {output_name}')
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    output_name = f'{file_address}_O3_plot.png'

    # saves plot
    plt.savefig(output_name, dpi=300)
    plt.close()

    ### Graphs like the wavelength_results graphs
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    plt.savefig(output_name, dpi=300)

    plt.close()