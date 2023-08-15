import numpy as np
import random, math, os
from joblib import Parallel, delayed
from utility import *

e_f = 4.401071
X = 100
XX = 22776
data = np.load('Egrid_'+str(X)+'_'+str(XX)+'.npy')
data = data[6:26]
kpoints = np.load('kw_'+str(X)+'_'+str(XX)+'.npy')

# Ideally, don't touch anything after this line

Nk = kpoints.shape[0]
# Define the band energies (128x56 matrix) and the Fermi energy E_Fermi
looper = data.shape[0]

band_energies = data
E_Fermi = e_f
# Create a function to calculate the Gamma contribution for a single iteration
def calculate_gamma(iteration, looper, Nk, band_energies, E_Fermi, kpoints):
    print(f"Executing {iteration} on pid {os.getpid()}")
    Gamma = 0.0
    for _ in range(iteration):
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
    return Gamma

# Set the number of iterations
nbr_samples_in_total = int(1e11)  # You can adjust this as needed

# Define the number of parallel processes/workers
nbr_parallel_blocks = 10

# Calculate the number of iterations per block, rounding up to the nearest integer
nbr_samples_per_block = math.ceil(nbr_samples_in_total / nbr_parallel_blocks)

# Calculate the Gamma contribution using Parallel and delayed
Gamma_contributions = Parallel(n_jobs=nbr_parallel_blocks, verbose = 11, backend='multiprocessing')(
    delayed(calculate_gamma)(nbr_samples_per_block, looper, Nk, band_energies, e_f, kpoints)
    for _ in range(nbr_parallel_blocks)
)

# Sum up the contributions to obtain the final Gamma
Gamma = sum(Gamma_contributions)

print("Final Auger =", Gamma, "for", nbr_samples_in_total)

