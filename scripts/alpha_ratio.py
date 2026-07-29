# This shows the relationship between the H-alpha broad and narrow ratio with their redshift.

import matplotlib.pyplot as plt
import numpy as np

# gets the data
oceans_id = np.array(['20504', '35829', '102364', '100424', '101393', '101208', '33842', '169045', '161695', '1794'])
f_narrow = np.array([2.61e-17, 5.95e-18, 2.53e-18, 4.30e-18, 3.90e-19, 7.70e-19, 1.90e-18, 1.05e-17, 7.63e-19, 8.58e-18])
f_broad = np.array([1.50e-16, 4.63e-17, 1.80e-17, 9.48e-18, 5.81e-18, 8.65e-18, 1.12e-17, 1.05e-17, 1.09e-18, 6.15e-18])
redshift = np.array([5.276, 6.684, 4.542, 4.953, 3.850, 5.682, 5.287, 5.239, 5.666, 3.681])

# gets the ratios
ratio = f_narrow / f_broad

# separates the standouts
mask_standout = np.isin(oceans_id, ['169045', '1794'])
mask_normal = ~mask_standout

plt.figure(figsize=(10, 7))

# plots using masks and arrays
plt.scatter(ratio[mask_normal], redshift[mask_normal], color='gray', alpha=0.7, s=120, label='LRDs')
plt.scatter(ratio[mask_standout], redshift[mask_standout], color='red', marker='*', s=200, edgecolor='black', label='Narrow Line Dominated')

# adds labels
for i in range(len(oceans_id)):
    if mask_standout[i]:
        plt.text(ratio[i] - 0.09, redshift[i] + 0.1, f"ID: {oceans_id[i]}", fontsize=11, fontweight='bold', va='center')
    else:
        plt.text(ratio[i] + 0.015, redshift[i], f"{oceans_id[i]}", fontsize=8, color='gray', va='center')

plt.title(r'H$\alpha$ Narrow/Broad Flux Ratio with Redshift (z)', fontsize=16)
plt.xlabel(r'Flux Ratio ($F_{narrow}$ / $F_{broad}$)', fontsize=14)
plt.ylabel('Redshift (z)', fontsize=14)
plt.legend()

plt.show()
plt.savefig('../final_products/H-alpha_ratio.png', dpi=300)
plt.close()