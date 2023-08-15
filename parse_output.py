#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:53:11 2022

@author: tanvir_chowdhury
"""
# copy this file to the directories kgrid_10, kgrid_20 for instance
import numpy as np
from pymatgen.io.vasp.outputs import BSVasprun, Eigenval
from pymatgen.electronic_structure.core import Spin

# read vasprun.xml
bs = BSVasprun("./vasprun.xml")
bandstructure = bs.get_band_structure(kpoints_filename="KPOINTS")
data = bandstructure.bands[Spin(1)]
ev = Eigenval("EIGENVAL")
print(f'Band matrix (Egrid) shape  = {data.shape}')

# read kpoints
kpoints = data.shape[1]
ga_points = [  bandstructure.kpoints[i].cart_coords for i in range(0,kpoints)]
ga_points = np.array(ga_points)
e_f = bandstructure.efermi # Fermi energy
print(f'Fermi energy = {round(e_f,3)} eV')
print(f'shape of the kpoint array = {ga_points.shape}. So, {ga_points.shape[0]} kpoints each with (kx,ky,kz)')

# read KPOINTS
k1 = np.loadtxt('KPOINTS',skiprows=3,usecols = 0)
X = int(k1)
XX = ev.nkpt
print("X = ", X)
print("XX = ", XX)
print(f'Number of bands = {ev.nbands}')
print('kgrid saved ...')
# write kgrid in a file
np.save('kgrid_'+str(X)+'_'+str(XX)+'.npy',ga_points)
print('Egrid saved ...')
np.save('Egrid_'+str(X)+'_'+str(XX)+'.npy',data)
# write Egrid in a file
print('k weight saved ...')
np.save('kw_'+str(X)+'_'+str(XX)+'.npy',ev.kpoints_weights)
# write kw grid in a file
