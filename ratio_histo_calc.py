# Finds ratio of OIII/Hg, plots results on a histogram in log scale

import os
import numpy as np
from astropy.io import fits
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

# List of exact target filenames
target_galaxies = [

    'f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits',
    'f170lp_g235h_s000169045_x1d_nodded-bg_P4_errescaled.fits'
]

target_data = {}

# loop only through the 3 ID's, ignore others
for filename in target_galaxies:
    file_address = os.path.join(data_folder, filename)
    print(f"Processing: {file_address}")

    # make sure no typos
    if not os.path.exists(file_address):
        print(f"File not found: {file_address}")
        continue

    # get the short ID
    galaxy_id = filename.split('_')[2]
    z_val = redshifts[galaxy_id]

    hdul = fits.open(file_address)
    wavelength_microns = hdul[1].data['Wavelength']
    flux_array = hdul[1].data['Flux']
    hdul.close()

    spec = lime.Spectrum.from_file(file_address, instrument='nirspec', redshift=z_val)
    spec.unit_conversion(wave_units_out='Angstrom', flux_units_out=u.erg / u.s / (u.cm ** 2))

    spec.fit.bands('H1_4340A', cont_source='adjacent')
    spec.fit.bands('O3_4363A', cont_source='adjacent')

    try:
        profile_flux_gamma = spec.frame.loc[['H1_4340A'], ['profile_flux']].iloc[0, 0]
        profile_flux_oxy = spec.frame.loc[['O3_4363A'], ['profile_flux']].iloc[0, 0]

        profile_flux_err_gamma = spec.frame.loc[['H1_4340A'], ['profile_flux_err']].iloc[0, 0]
        profile_flux_err_oxy = spec.frame.loc[['O3_4363A'], ['profile_flux_err']].iloc[0, 0]

        # Calculates ratio and log ratio
        ratio = profile_flux_oxy / profile_flux_gamma
        log_ratio = np.log10(ratio)

        # Calculates error propagation
        fractional_err_oxy = profile_flux_err_oxy / profile_flux_oxy
        fractional_err_gamma = profile_flux_err_gamma / profile_flux_gamma
        ratio_err = ratio * np.sqrt(fractional_err_oxy ** 2 + fractional_err_gamma ** 2)
        log_ratio_err = ratio_err / (ratio * np.log(10))

        target_data[galaxy_id] = {'log_val': log_ratio, 'error': log_ratio_err}


    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Plots shaded regions
plt.axvspan(xmin=-0.43933269, xmax=1.0, color='red', alpha=0.1, linewidth=2, label='BLAGN Region')
plt.axvspan(xmin=-0.43933269, xmax=-0.37892762, color='yellow', alpha=0.2, linewidth=2, label='Composite Region')
plt.axvspan(xmin=-1.64839692, xmax=-0.37892762, color='green', alpha=0.1, linewidth=2, label='SF Region')

# info for histo plot
plot_info = {

    's000001794': {'color': 'purple', 'height': 0.5},
    's000169045': {'color': 'blue', 'height': 0.6}
}

for gal_id, data in target_data.items():
    val = data['log_val']
    err = data['error']
    c = plot_info[gal_id]['color']
    arrow_height = plot_info[gal_id]['height']

    # Plots main lines
    plt.axvline(x=val, color=c, linestyle='--', label=gal_id)

    # Plots error bar
    left_bound = val - err
    right_bound = val + err

    plt.errorbar(x=val,
                 y=arrow_height,
                 xerr=err,
                 fmt='none',
                 ecolor=c,
                 capsize=3,
                 capthick=1.5,
                 linewidth=1.5)

# Labels
plt.xlabel(r'$\log_{10}([\mathrm{OIII}] / \mathrm{Hg})$')
plt.yticks([])
plt.legend(loc='upper right')

plt.savefig('in_paper/final_lineplot.png', dpi=300)
plt.show()
plt.close()