import astropy.io.fits as fits
import matplotlib.pyplot as plt
from pathlib import Path

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'

file_235 = data_folder / 'f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits'
file_395 = data_folder / 'f290lp_g395h_s000001794_x1d_nodded-bg_P1_errescaled.fits'

# Make canvas
plt.figure(figsize=(12, 6))

if file_235.exists():
    hdul_235 = fits.open(file_235)
    data_235 = hdul_235[1].data
    plt.plot(data_235['Wavelength'], data_235['Flux'],
             drawstyle='steps-mid', color='crimson', label='Filter G235H', alpha=0.8)
    hdul_235.close()

if file_395.exists():
    hdul_395 = fits.open(file_395)
    data_395 = hdul_395[1].data
    plt.plot(data_395['Wavelength'], data_395['Flux'],
             drawstyle='steps-mid', color='royalblue', label='Filter G395H', alpha=0.8)
    hdul_395.close()

# Label graph
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('Combined JWST Spectrum - Source ID: s000001794')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

output_name = "s000001794_combined_spectrum.png"
plt.savefig(output_name, dpi=300)
plt.close()
