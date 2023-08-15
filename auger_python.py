import numpy as np
import time
from scipy.special import expit

begin = time.perf_counter()
e_f = 4.401071
constants = {'h':4.1357e-15,'volume':73.26286645969724e-24}


data = np.load('Egrid_100_22776.npy')
data = data[6:26]
kpoints = np.load('kw_100_22776.npy')

# Ideally, don't touch anything after this line
# Define the output saving interval in seconds (1 hour = 3600 seconds)
saving_interval = 1800
current_time = time.time()

# Initialize a variable to keep track of the time of the last save
last_save_time = current_time

Nk = kpoints.shape[0]
# Define the band energies (128x56 matrix) and the Fermi energy E_Fermi
band_energies = data
E_Fermi = e_f


def fermi_dirac(E, E_Fermi, k_B=8.617333262145e-5, T=300):
    return expit((E_Fermi - E) / (k_B * T))


# Define the Fermi-Dirac distribution function
#def fermi_dirac(E, E_Fermi, k_B=8.617333262145e-5, T=300):
#    return 1.0 / (1.0 + np.exp((E - E_Fermi) / (k_B * T)))

# Define the product function P_1234
def P_1234(E, f):
    return (1 - f[0]) * (1 - f[1]) * f[2] * f[3]

# Define the Kronecker delta function δ(E_1+E_2-E_3-E_4)
# change it to gaussian delta
#def delta_func(E1, E2, E3, E4):
#    return 1.0 if abs(E1 + E2 - E3 - E4) < 1e-12 else 0.0

def delta_func(E1, E2, E3, E4, sigma=0.01):
   # Computes the Gaussian model of the delta function.
    return np.exp(-(E1 + E2 - E3 - E4)**2 / (2 * sigma**2))
# Perform the summation over all combinations of four bands and k-points

looper = data.shape[0]
Gamma = 0.0
for i in range(looper):
    for j in range(looper):
        for k in range(looper):
            for l in range(looper):
                for m in range(Nk):
                    delta = delta_func(band_energies[i,m], band_energies[j,m], band_energies[k,m], band_energies[l,m])
                    if delta >= 0.9:
                      f = [fermi_dirac(band_energies[i,m], E_Fermi),
                         fermi_dirac(band_energies[j,m], E_Fermi),
                         fermi_dirac(band_energies[k,m], E_Fermi),
                         fermi_dirac(band_energies[l,m], E_Fermi)]
                      P = P_1234(band_energies[[i,j,k,l], m], f)
                      Gamma += P * delta * kpoints[m] ** 4
                      # Check if it's time to save the output
                      current_time = time.time()
                      if current_time - last_save_time >= saving_interval:
                      # Save the output to a file or perform any necessary operations
                        print(f'i={i},j={j},k={k},l={l}\n')
                        print(f'm={m}\n')
                        print("Auger =", Gamma, 'at', current_time,'\n')

                        # Update the last save time
                        last_save_time = current_time
end = time.perf_counter()
print("Final Auger =", format(Gamma,".2e"), 'at', end - begin,'\n')
