# Finds ratio of OIII/Hg, plots results on a histogram in log scale

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

all_ratios = []

# dictionary for three specific IDs
target_galaxies = ['s000101393', 's000001794', 's000169045']
target_data = {}

for file_address in glob.glob(data_folder + '*.fits'):
    print(file_address)
    # file_address = 'data/reextrac2/f170lp_g235h_s000020504_x1d_nodded-bg_P1_errescaled.fits'

    galaxy_id = file_address.split('_')[2]
    z_val = redshifts[galaxy_id]

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

        profile_flux_err_gamma = spec.frame.loc[['H1_4340A'], ['profile_flux_err']].iloc[0, 0]
        profile_flux_err_oxy = spec.frame.loc[['O3_4363A'], ['profile_flux_err']].iloc[0, 0]

        # Calculate ratio and log ratio
        ratio = profile_flux_oxy / profile_flux_gamma
        log_ratio = np.log10(ratio)
        all_ratios.append(ratio)

        # finds error propagation
        fractional_err_oxy = profile_flux_err_oxy / profile_flux_oxy
        fractional_err_gamma = profile_flux_err_gamma / profile_flux_gamma
        ratio_err = ratio * np.sqrt(fractional_err_oxy ** 2 + fractional_err_gamma ** 2)
        log_ratio_err = ratio_err / (ratio * np.log(10))

        if galaxy_id in target_galaxies:
            target_data[galaxy_id] = {'log_val': log_ratio, 'error': log_ratio_err}

    except Exception as e:
        print(e)

# cleans ratios, no nan
clean_ratios = np.array(all_ratios)
clean_ratios = clean_ratios[(np.isfinite(clean_ratios)) & (clean_ratios > 0)]
log_ratios = np.log10(clean_ratios)
clean_log_ratios = log_ratios[(log_ratios < 1)]

# Checks the ratios
#print(all_ratios)
#print(clean_ratios)
#print(log_ratios)
#print(clean_log_ratios)

# Plots shaded regions
plt.axvspan(xmin=-0.43933269, xmax=1.0, color='red', alpha=0.1, linewidth=2, label='BLAGN Region')
plt.axvspan(xmin=-0.43933269, xmax=-0.37892762, color='yellow', alpha=0.1, linewidth=2, label='Composite Region')
plt.axvspan(xmin=-1.64839692, xmax=-0.37892762, color='green', alpha=0.1, linewidth=2, label='SF Region')

# gives each fits a certain color
plot_info = {
    's000101393': {'color': 'orange', 'height': 0.25},
    's000001794': {'color': 'purple', 'height': 0.5},
    's000169045': {'color': 'blue',   'height': 0.75}
}

for gal_id, data in target_data.items():
    val = data['log_val']
    err = data['error']
    c = plot_info[gal_id]['color']
    arrow_height = plot_info[gal_id]['height']

    # Plots the main lines
    plt.axvline(x=val, color=c, linestyle='--', label=gal_id)

    # Calculates the left and right bounds of the error
    left_bound = val - err
    right_bound = val + err

    # Draws the double-headed arrow across the error
    plt.annotate('',
                 xy=(left_bound, arrow_height),  # Start point of the arrow
                 xytext=(right_bound, arrow_height),  # End point of the arrow
                 arrowprops=dict(arrowstyle='<->', color=c, linewidth=1.5, shrinkA=0, shrinkB=0))

'''plt.axvline(x=-0.5335600605894151, color = 'orange', linestyle='--', label = 's000101393')
plt.axvline(x=-0.4486212610729128, color = 'purple', linestyle='--', label = 's000001794')
plt.axvline(x=-0.23118045243916688, color = 'blue', linestyle='--', label = 's000169045')
'''

# labels
plt.xlabel(r'$\log_{10}([\mathrm{OIII}] / \mathrm{Hg})$')
plt.ylabel('Count')
plt.legend(loc='upper right')

plt.savefig(f'final_histogram.png', dpi=300)
plt.show()
plt.close()