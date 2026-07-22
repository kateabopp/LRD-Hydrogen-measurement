# Calculates sigma and observed wavelength using given FWHMs

import numpy as np
import astropy.units as u
import astropy.constants
from astropy.constants import c


z_list = [5.666, 5.276, 6.684, 4.953, 5.287, 5.239]
# 3.681, 4.542, 3.850, 5.682
fwhm_list = [1134, 2423, 2477, 1636, 2324, 1909]


c_kms = c.to(u.km / u.s)

for z, FWHM in zip(z_list, fwhm_list):
    observe_wave = 4341.7 * (1 + z)
    Sigma = (FWHM / (2 * np.sqrt(2 * np.log(2)) * (observe_wave / c_kms)))
    sigma_micro = Sigma / 10000

    print(f'z: {z:<6.3f} | Observed wave = {observe_wave:<10.1f} | FWHM: {FWHM:<6.1f} | Sigma: {sigma_micro}')