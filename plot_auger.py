#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 12:50:11 2023

@author: shah
"""

import numpy as np
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size' : 14})

looper = 20.0
x = np.array([1e7, 1e8, 1e9, 1e10, 1e11])
y = np.array([3.18E-55, 4.73E-30, 1.31e-13, 4.56E-13, 3.9e-12])
z = np.array([6.979E-62, 7.245E-40, 8.88e-28, 5.248E-24, 3.16e-15])
b = np.array([7.02E-93, 3.89E-56, 8.72e-42, 4.68E-28, 1.15e-26])
c = np.array([2.91E-71, 2.20E-60, 2.76e-43, 2.72E-33])

y *= (looper ** 4 * 47 ** 4) / x
z *= (looper ** 4 * 256 ** 4) / x
b *= (looper ** 4 * 3107 ** 4) / x
#c *= (looper ** 4 * 22776 ** 4) / x
fig, ax1 = plt.subplots(figsize=(5, 5))

ax1.loglog(x,y,marker='^', label=r'$10\times10\times10$', mfc='w', markersize=12,linewidth=3.5)
ax1.loglog(x,z,marker='o', label=r'$20\times20\times20$', mfc='w', markersize=12,linewidth=3.5)
#ax1.loglog(x,b,marker='s', label=r'$50\times50\times50$', mfc='w', markersize=12,linewidth=3.5)
#ax1.loglog(x,c,marker='D', label=r'$100\times100\times100$', mfc='w', markersize=12,linewidth=3.5)

ax1.set_xlabel('Monte-Carlo Steps')
ax1.set_ylim((pow(10, -84), pow(10, -2)))
#####
#plot params
ax1.minorticks_on()
ax1.tick_params(axis="both", direction='in',which='minor', bottom=True, top=True, left=True, right=True)
ax1.tick_params(direction='in',which='major', length=10, bottom=True, top=True, left=True, right=True)
#####
#plt.text(38.9, 3.37e-29,'Exp')
#plt.text(0.05,1.9,'Did not converge yet')
#plt.text(0.05,3.8,'Did not converge yet')
#plt.axhspan(10e-22,10e-34, color='black', alpha=0.2)
ax1.set_title('log-log plot')
ax1.legend(loc='lower right')

# Create a twin y-axis on the right side
ax2 = ax1.twinx()
ax2.set_yscale('log')
ax2.set_ylim((pow(10, -84), pow(10, -2)))
ax2.tick_params(axis='y', which='both', direction='in', length=10, left=True, right=True)

plt.savefig('/home/shah/Pictures/dft_bands/oj.png', dpi=300,bbox_inches="tight")
plt.show()
