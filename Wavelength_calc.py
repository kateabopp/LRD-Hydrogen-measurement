import numpy as np
from astropy.io import fits
from pathlib import Path
import lime
import matplotlib.pyplot as plt

#This makes the info chart (from lime website)
print(lime.lineDB.frame.loc['H1_4340A'])
print(f'\nDatabase default shape {lime.lineDB.get_shape()}, profile {lime.lineDB.get_profile()} and units {lime.lineDB.get_units()}')

data_folder = Path('data/reextrac2')
output_folder = Path('data/wavelength_results')

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

for file_address in data_folder.glob('*.fits'):
    z_val = next((v for k, v in redshifts.items() if k in file_address.name), 0.0)

    hdul = fits.open(file_address)
    wavelength_microns = hdul[1].data['Wavelength']
    flux_array = hdul[1].data['Flux']
    hdul.close()

    # https://lime-stable.readthedocs.io/en/latest/1_introduction/4_lines_database.html
    spec = lime.Spectrum.from_file(file_address, instrument='nirspec', redshift=z_val)

    spec.unit_conversion(wave_units_out='Angstrom')
    spec.fit.bands('H1_4340A', cont_source='adjacent')

    spec.plot.bands(rest_frame=True, show_cont=False)

    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    output_name = output_folder / f"{file_address.stem}_spectrum.png"
    plt.savefig(output_name, dpi=300)

    plt.clf()
    plt.close()

