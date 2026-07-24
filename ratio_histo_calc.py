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

        ratio = profile_flux_oxy / profile_flux_gamma
        print(f'For fits: {file_address}, Gamma emission is: {profile_flux_gamma}, Oxygen 3 emission is: {profile_flux_oxy}')

        # Print log ratio before plotting
        log_ratio = np.log10(ratio)
        print(f'Ratio (OIII/Hg) is: {log_ratio}')

        all_ratios.append(ratio)

    except Exception as e:
        print(e)

# cleans ratios, no nan
clean_ratios = np.array(all_ratios)
clean_ratios = clean_ratios[(np.isfinite(clean_ratios)) & (clean_ratios > 0)]

log_ratios = np.log10(clean_ratios)
clean_log_ratios = log_ratios[(log_ratios < 1)]

# Checks the ratios
print(all_ratios)
print(clean_ratios)
print(log_ratios)
print(clean_log_ratios)

plt.hist(clean_log_ratios, bins=8, edgecolor='black')

plt.axvspan(xmin=-0.43933269, xmax=1.0, color='red', alpha=0.3, label='BLAGN Region')
plt.axvspan(xmin=-0.43933269, xmax=-0.37892762, color='yellow', alpha=0.2, linewidth=2, label='Composite Region')
plt.axvspan(xmin=-1.64839692, xmax=-0.37892762, color='green', alpha=0.2, linewidth=2, label='SF Region')

# labels
plt.xlabel(r'$\log_{10}([\mathrm{OIII}] / \mathrm{Hg})$')
plt.ylabel('Count')
plt.legend(loc='upper right')

plt.savefig(f'test_histo.png', dpi=300)
plt.show()
plt.close()