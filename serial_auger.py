import time
import numpy as np
import random
from utility import *

i_min = 6 # copy it from band_info.txt
i_max = 26 # copy it from band_info.txt
E_Fermi = 4.401071 # copy it from band_info.txt
X = 100
XX = 22776
data = np.load('Egrid_'+str(X)+'_'+str(XX)+'.npy')
data = data[i_min:i_max]
kpoints = np.load('kw_'+str(X)+'_'+str(XX)+'.npy')

# Ideally, don't touch anything after this line

Nk = kpoints.shape[0]
# Define the band energies (128x56 matrix) and the Fermi energy E_Fermi
looper = data.shape[0]
band_energies = data
# Ideally, don't touch anything after this line
# Define the output saving interval in seconds (1 hour = 3600 seconds)
saving_interval = 1800
current_time = time.time()

# Initialize a variable to keep track of the time of the last save
last_save_time = current_time

Gamma = 0.0

total_iterations = [1_0000_0000_00] #np.logspace(7, 9, 3).astype(int)

for iter_ in total_iterations:
    for _ in range(iter_):
        i = random.randint(0, looper-1)
        j = random.randint(0, looper-1)
        k = random.randint(0, looper-1)
        l = random.randint(0, looper-1)
        m = random.randint(0, Nk-1)
        n = random.randint(0, Nk-1)
        o = random.randint(0, Nk-1)
        p = random.randint(0, Nk-1)
    
        delta = delta_func(band_energies[i, m], band_energies[j, n], band_energies[k, o], band_energies[l, p])
        if delta >= 0.9:
            f = [fermi_dirac(band_energies[i, m], E_Fermi),
                 fermi_dirac(band_energies[j, n], E_Fermi),
                 fermi_dirac(band_energies[k, o], E_Fermi),
                 fermi_dirac(band_energies[l, p], E_Fermi)]
            P = P_1234(band_energies[[i, j, k, l], [m, n, o, p]], f)
            Gamma += P * delta * kpoints[m] * kpoints[n] * kpoints[o] * kpoints[p]
                   # Check if it's time to save the output
            current_time = time.time()
            if current_time - last_save_time >= saving_interval: 
                print(f'i={i},j={j},k={k},l={l}\n')
                print(f'm={m},n={n},o={o},p={p}\n')
                print("Auger =", Gamma, 'at', current_time,'\n')
    
                # Update the last save time
                last_save_time = current_time
    print("Final Auger =", Gamma, "for",iter_)
