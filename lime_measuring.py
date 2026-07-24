# Uses lime to make measurement plot. NOT SPECTRA

import numpy as np
from astropy.io import fits
from pathlib import Path
import lime
import astropy
import matplotlib.pyplot as plt

current_folder = Path(__file__).parent
data_folder = current_folder / 'data' / 'reextrac2'

# fits ID with redshift
redshifts = {
    's000161695': 5.666,
    's000020504': 5.276,
    's000035829': 6.684,
    's000100424': 4.953,
    's000033842': 5.287,
    's000169045': 5.239,
    's000001794': 3.681,
    's000102364': 4.542,
    's000101393': 3.850,
    's000101208': 5.682,
}


for file_address in data_folder.glob('*.fits'):
    # Create the observation, stackoverflow
    z_val = next((v for k, v in redshifts.items() if k in file_address.name))

    spec = lime.Spectrum.from_file(file_address, instrument='nirspec', redshift=z_val)

    spec.fit.continuum(degree_list=[3, 6, 6], emis_threshold=[3, 2, 1.5], plot_steps=True, log_scale=True)
    candidate_lines = spec.retrieve.lines_frame()
    matched_lines = spec.infer.peaks_troughs(candidate_lines, emission_type=True, sigma_threshold=3, plot_steps=True, log_scale=True)
    spec.fit.bands('H1_4340A_b', cont_source='adjacent')

    try:
        profile_flux = spec.frame.loc[['H1_4340A_b'], ['profile_flux']].iloc[0, 0]
        print(profile_flux)
    except:
        print("No profile flux found")