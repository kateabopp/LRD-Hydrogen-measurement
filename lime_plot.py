import numpy as np
from astropy.io import fits
from pathlib import Path
import matplotlib.pyplot as plt
import lime

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'

jwst_file = data_folder / 'f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits'

hdul = fits.open(jwst_file)
wavelength_array = hdul[1].data['Wavelength']
flux_array = hdul[1].data['Flux']
hdul.close()

shoc579 = lime.Spectrum(wavelength_array, flux_array, redshift=3.681)

shoc579.plot.spectrum(rest_frame=False)

plt.savefig('f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits.png', dpi=300)
plt.close()