# This plots the final plot using the SMC dust curve

import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
import astropy.constants as const
from pathlib import Path
from dust_extinction.averages import G24_SMCAvg

# output goes to correct folder
current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'
final_folder = current_folder / 'final_plots'
final_folder.mkdir(parents=True, exist_ok=True)

# from paper - real data
# fits IDs: 161695, 20504, 35829, 169045
narrow_Ha_flux = np.array([7.63e-19, 2.61e-17, 5.95e-18, 1.05e-17])
narrow_Hb_flux = np.array([2.31e-19, 2.05e-18, 9.13e-19, 3.11e-18])

# PLACEHOLDER - Gotta replace data
narrow_Hg_flux = np.array([6.4510757e-06, 7.382846e-06, 6.57718e-06, 4.0092532e-05])

log_HaHb_narrow = np.log10(narrow_Ha_flux / narrow_Hb_flux)
log_HgHa_narrow = np.log10(narrow_Hg_flux / narrow_Ha_flux)

# PLACEHOLDERS - not real data
log_HgHa_narrow_err = np.array([0.03, 0.02, 0.04, 0.03])
log_HaHb_narrow_err = np.array([0.05, 0.04, 0.06, 0.05])

# broad data - real data
broad_Ha_flux = np.array([1.09e-18, 1.50e-16, 4.63e-17, 1.05e-17]) * (u.erg / (u.s * u.cm**2))
broad_Hb_flux = np.array([4.09e-19, 1.14e-17, 8.17e-18, 1.98e-18]) * (u.erg / (u.s * u.cm**2))

# these are the limits in just Janskys - real data
broad_Hg_limit_jy = np.array([9.27e-09, 8.08e-09, 1.47e-08, 7.90e-09])

### Is this needed? can I change it to make it easier to read?
# 2000 is PLACEHOLDER for other FWHM vals - not sure what the best way to do this is
line_width_velocity = np.array([2000, 2000, 2000, 2000]) * (u.km / u.s)

# Converts velocity width to frequency width (Hz) at the H-gamma wavelength
rest_freq_Hg = (const.c / (4341 * u.AA)).to(u.Hz)
line_width_hz = (line_width_velocity / const.c) * rest_freq_Hg
###

# multiplies Jy by Hz to get integrated flux, then convert to cgs
broad_Hg_flux_cgs = (broad_Hg_limit_jy) * (u.erg / (u.s * u.cm**2))

# calculates Broad Ratios
log_HgHa_broad = np.log10(broad_Hg_flux_cgs.value / broad_Ha_flux.value)
log_HaHb_broad = np.log10(broad_Ha_flux.value / broad_Hb_flux.value)

# intrinsic values from paper
intrinsic_HaHb = 2.86
intrinsic_HgHa = 0.163

log_HaHb_intrinsic = np.log10(intrinsic_HaHb)
log_HgHa_intrinsic = np.log10(intrinsic_HgHa)

# SMC dust law data - gets in correct unit (inverse microns)
wave_Ha_inv = (1 / (6565 * u.AA)).to(1 / u.micron)
wave_Hb_inv = (1 / (4861 * u.AA)).to(1 / u.micron)
wave_Hg_inv = (1 / (4341 * u.AA)).to(1 / u.micron)

Av = np.linspace(0, 8, 50)
smc = G24_SMCAvg()

# gets the line for the SMC dust law
y_line_smc = log_HaHb_intrinsic - 0.4 * Av * (smc(wave_Ha_inv) - smc(wave_Hb_inv))
x_line_smc = log_HgHa_intrinsic - 0.4 * Av * (smc(wave_Hg_inv) - smc(wave_Ha_inv))

# Plots
plt.figure(figsize=(8, 6))

# Narrow ratios
plt.errorbar(log_HgHa_narrow, log_HaHb_narrow, xerr=log_HgHa_narrow_err, yerr=log_HaHb_narrow_err,
             fmt='s', color='black', markerfacecolor='black', markeredgecolor='black',
             capsize=3, label='Narrow ratios', zorder=4)

# Broad ratios
plt.errorbar(log_HgHa_broad, log_HaHb_broad, xerr=0.08, yerr=0.08, xuplims=True,
             fmt='o', color='firebrick', markerfacecolor='red', markeredgecolor='darkred',
             capsize=0, label='Broad ratios', zorder=4)

# Plots SMC Dust Law
plt.plot(x_line_smc, y_line_smc, color='gold', linestyle='--', linewidth=2, label='SMC Dust Law', zorder=2)

# Label for Extinction Direction
plt.annotate('Increasing $A_V$', xy=(-1.4, 0.7), xytext=(-1.1, 0.4),
             arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
             rotation=-40, ha='center', va='center', fontsize=12)

# Shaded bands
plt.axvline(x=log_HgHa_intrinsic, color='grey', alpha=0.25, linewidth=15, zorder=1)
plt.axhline(y=log_HaHb_intrinsic, color='grey', alpha=0.25, linewidth=15, zorder=1)

plt.xlabel(r'$\log_{10}(\text{H}\gamma/\text{H}\alpha)$', fontsize=14)
plt.ylabel(r'$\log_{10}(\text{H}\alpha/\text{H}\beta)$', fontsize=14)
plt.xlim(-2.4, -0.4)
plt.ylim(0.1, 1.7)
plt.legend(loc='lower left', frameon=False, fontsize=12)
plt.tick_params(axis='both', direction='in', top=True, right=True, length=6)

plt.tight_layout()

# saves the plot
plt.savefig(final_folder / 'final_plot_test.png', dpi=300)
plt.show()