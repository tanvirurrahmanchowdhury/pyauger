#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 13:53:11 2023

@author: tanvir_chowdhury
"""
import numpy as np
import time
from pymatgen.io.vasp.outputs import BSVasprun, Eigenval
from pymatgen.electronic_structure.core import Spin
from utility import *

# read vasprun.xml
bs = BSVasprun("./vasprun.xml")
bandstructure = bs.get_band_structure(kpoints_filename="KPOINTS")
data = bandstructure.bands[Spin(1)]
ev = Eigenval("EIGENVAL")
print(f'Band matrix (Egrid) shape  = {data.shape}')

ef = round(bandstructure.efermi,2) # Fermi energy


fn = np.sum(fermi_dirac(data,ef), axis = 1)

boolean_array = (fn != 0)

# Find the index of the first False value
first_false_index = np.argmax(~boolean_array)

print(f'i_min = {first_false_index-10}')
print(f'i_max = {first_false_index+10}')
a = list([first_false_index-10, first_false_index+10, ef])
b = list(['i_min','i_max', 'E_Fermi'])
#writing data into a file
with open('band_info.txt', 'w') as f:
    for f1, f2 in zip(b, a):
        print(f1, f2, file=f)

