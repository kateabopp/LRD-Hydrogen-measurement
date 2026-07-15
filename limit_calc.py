import numpy as np
import astropy.units as u
import astropy.constants
from astropy.constants import c


# This is your range of wavelengths calculated in the previous step. (Kelcey doc)
'''Wave_array= [0.49882810, 1.13207095, 0.94523940, 0.80584327, 1.08391650,0.89721000] 
# This array is the values for the flux error at all the points in your wavelength array. (Kelcey doc)
Error_array = []

D_lambda = np.median (np.diff(Wave_array))
Integrated_flux_sigma =D_lambda * np.sqr(np.sum(Error_array**2))
Three_sigma_limit = 3*Integrated_flux_sigma
'''

z_list = [5.666, 5.276, 6.684, 4.953, 5.287, 5.239]
# 3.681, 4.542, 3.850, 5.682
fwhm_list = [1134, 2423, 2477, 1636, 2324, 1909]


c_kms = c.to(u.km / u.s)

for z, FWHM in zip(z_list, fwhm_list):
    observe_wave = 4341.7 * (1 + z)
    Sigma = (FWHM / (2 * np.sqrt(2 * np.log(2)) * (observe_wave / c_kms)))
    sigma_micro = Sigma / 10000

    print(f'z: {z:<6.3f} | Observed wave = {observe_wave:<10.1f} | FWHM: {FWHM:<6.1f} | Sigma: {sigma_micro}')