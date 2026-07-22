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

# This program plots the final graph similar to the paper using the SMC line - it doesn't work correctly though

'''import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from pathlib import Path
from dust_extinction.averages import G24_SMCAvg

# Sends final result to correct directory
current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'
final_folder = current_folder / 'final_plots'

fits_files = list(data_folder.glob('*.fits'))

# PLACEHOLDERS I USED TO TEST OUT - replac with real data later
log_HaHb_narrow = np.array([])
log_HaHb_narrow_err = np.array([])

log_HgHa_narrow = np.array([-0.78, -0.82, -0.75, -0.68, -0.71, -0.65])
log_HgHa_narrow_err = np.array([0.03, 0.02, 0.04, 0.03, 0.02, 0.03])

# The broad limit I found - 3 integrated sigma - janskys
broad_Hg_limit = np.array([9.2719258e-09, 8.0836847e-09, 1.47916168e-08, 1.109627e-08, 1.4782255e-08, 7.9090569e-09])

redshifts = np.array([5.666, 5.276, 6.684, 4.953, 5.287, 5.239])

# Broad h-alphas and h-betas from paper - which is in erg/s/cm^2
broad_Ha_flux = np.array([1.09e-18, 1.50e-16, 4.63e-17, 9.48e-18, 1.12e-17, 1.05e-17]) * (u.erg / (u.s * u.cm**2))
broad_Hb_flux = np.array([3.81e-19, 5.21e-17, 1.55e-17, 3.10e-18, 3.86e-18, 3.44e-18])

# Gets correct units
wave_Hg_obs_meters = (4341.7 * 1e-10) * (1 + redshifts)
frequency_Hg = 3e8 / wave_Hg_obs_meters

# Converts Janskys to erg/s/cm^2
broad_Hg_limit_cgs = broad_Hg_limit * 1e-23 * frequency_Hg


# h-gamma/h-alpha ratio for the broad
log_HgHa_broad = np.log10(broad_Hg_limit / broad_Ha_flux)

# h-alpha/h-beta ratio for the broad
log_HaHb_broad = np.log10(broad_Ha_flux / broad_Hb_flux)


# ALL AFTER THIS WORKS

# Found in OCEANS paper
intrinsic_HaHb = 2.86
intrinsic_HgHa = 0.163

log_HaHb_intrinsic = np.log10(intrinsic_HaHb)
log_HgHa_intrinsic = np.log10(intrinsic_HgHa)

# Constants in Angstroms
wave_Ha = 6565 * u.AA
wave_Hb = 4861 * u.AA
wave_Hg = 4341 * u.AA

smc = G24_SMCAvg()
k_Ha = smc(wave_Ha)
k_Hb = smc(wave_Hb)
k_Hg = smc(wave_Hg)

Av = np.linspace(0, 8, 50)

# SMC calc
y_line = log_HaHb_intrinsic - 0.4 * Av * (k_Ha - k_Hb)
x_line = log_HgHa_intrinsic - 0.4 * Av * (k_Hg - k_Ha)

# Should add other laws later!
# LMC calc

# Maybe Milky Way calc?

# Plots on graph
plt.figure(figsize=(8, 6))

# Narrow points are squares
plt.errorbar(log_HgHa_narrow, log_HaHb_narrow, xerr=log_HgHa_narrow_err, yerr=log_HaHb_narrow_err, fmt='s', color='blue', label='Narrow Components', zorder=3)

# Broad points are circles
# Fix xuplims
plt.errorbar(log_HgHa_broad, log_HaHb_broad, xerr=0.08, yerr=0.08, xuplims=True, fmt='o', color='purple', label='Broad Components', zorder=3)

plt.plot(x_line, y_line, label='SMC Dust Law', color='red', linestyle='--', linewidth=2)

# Vertical shaded band for H-gamma/H-alpha
plt.axvline(x=log_HgHa_intrinsic, color='grey', alpha=0.50, linewidth=12, zorder=1)
# Horizontal shaded band for H-alpha/H-beta
plt.axhline(y=log_HaHb_intrinsic, color='grey', alpha=0.50, linewidth=12, zorder=1)

plt.xlabel(r'$\log_{10}(\text{H}\gamma/\text{H}\alpha)$')
plt.ylabel(r'$\log_{10}(\text{H}\alpha/\text{H}\beta)$')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

plt.savefig(final_folder, dpi=300)
plt.close()
'''
