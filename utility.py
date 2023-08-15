import numpy as np
from scipy.special import expit

def absolute_value_squared(v1, v2):
    return np.abs(v1 - v2)**2

def overlap_integral(bra, ket):
    bra = np.array(bra)
    ket = np.array(ket)
    
    if bra.shape != ket.shape:
        raise ValueError("Bra and ket vectors must have the same shape.")
    
    result = np.dot(np.conj(bra), ket)
    return result

def fermi_dirac(E, E_Fermi, k_B=8.617333262145e-5, T=300):
    return expit((E_Fermi - E) / (k_B * T))

# Define the product function P_1234
def P_1234(E, f):
    return (1 - f[0]) * (1 - f[1]) * f[2] * f[3]

def delta_func(E1, E2, E3, E4, sigma=0.01):
   # Computes the Gaussian model of the delta function.
    return np.exp(-(E1 + E2 - E3 - E4)**2 / (2 * sigma**2))

if __name__ == '__main__':
   kpoints = np.load('kgrid_10_47.npy')
   print(kpoints.shape)
   print(absolute_value_squared(kpoints[5],kpoints[10]))
