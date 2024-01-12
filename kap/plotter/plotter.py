#!/usr/bin/env python

import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def parse(fname):
    nY, nX = np.loadtxt(fname, max_rows=1, skiprows=3, unpack=True, dtype=int)
    data = np.loadtxt(fname, skiprows=4)
    data = np.reshape(data, ((nX, nY, -1)))
    Yran = np.array(data[0,:,0])
    Xran = np.array(data[:,0,1])
    data = np.swapaxes(data, 0, 1)
    return data, Yran, Xran


with open('kap_plotter.dat') as f:
    title = f.readline().strip()
    xlabel = f.readline().strip()
    ylabel = f.readline().strip()

kapDT, Yran, Xran = parse('kap_plotter.dat')

# set up plot and labels
fig, ax = plt.subplots(figsize=(4,3))
ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_xlim(Xran.min(), Xran.max())
ax.set_ylim(Yran.min(), Yran.max())

# set up color map
cmap = copy.copy(mpl.cm.get_cmap("coolwarm"))
cmap.set_over('white')
cmap.set_under('black')

# set color bar limits
# None will auto-set limits
cbar_min = -16
cbar_max = 2

pcol = ax.pcolormesh(Xran, Yran, kapDT[...,2], shading='nearest', cmap=cmap, vmin=cbar_min, vmax=cbar_max)
pcol.set_edgecolor('face')
cax = fig.colorbar(pcol, extend='both')
cax.set_label('')

# if x-y is logRho-logT, plot edges of logR
if(xlabel=='log10(Rho)' and ylabel=='log10(T)'):
    logRho = Xran
    logR_max = 1
    logR_min = -8
    logT_max = (logRho - logR_min + 18)/3
    logT_min = (logRho - logR_max + 18)/3
    ax.plot(logRho,logT_max,c='k',ls='-.',alpha=0.5)
    ax.plot(logRho,logT_min,c='k',ls='-.',alpha=0.5)
    #ax.text(-5,7.1,r'logR=-8',rotation=53,fontsize='small')
    

# save figure
fig.savefig('kap_plotter.png', dpi=300)

plt.show()
