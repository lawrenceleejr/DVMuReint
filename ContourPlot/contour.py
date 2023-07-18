#!/usr/bin/env python

import os,sys
# import ROOT
import numpy as np
import scipy
from scipy.interpolate import griddata
from scipy import signal
import matplotlib.pyplot as plt
import math


# f = ROOT.TFile("outputPlots_220822.root")

from numpy import genfromtxt
my_data = genfromtxt('MET_normalized_num_evts.csv', delimiter=',',skip_header=1)

# print(my_data)

plottingRange = (-3,2,400,2000)
# plottingRange = (2350,2470,6800,20000)
# grid_x, grid_y = np.mgrid[2300:2500:100j, 6000:10000:100j]
grid_x, grid_y = np.mgrid[plottingRange[0]:plottingRange[1]:200j,\
                            plottingRange[2]:plottingRange[3]:200j]


# f.ls()

contourlevel = 3

# for itype in ["MPA","SSA"]:
#     for ichip in range(8):

# h = f.Get(f"pulseShape_{itype}_{ichip}")
# h.Smooth(2,"k3a")

# print(dir(h))

# print(grid_x, grid_y)

fig, ax = plt.subplots()


points = []
zvalues = []

# for ibinx in range(h.GetNbinsX()):
#     for ibiny in range(h.GetNbinsY()):
#         # if h.GetYaxis().GetBinCenter(ibiny) > 10e3 or h.GetYaxis().GetBinCenter(ibiny) < 6e3:
#             # continue
#         points.append( (h.GetXaxis().GetBinCenter(ibinx), h.GetYaxis().GetBinCenter(ibiny)) )
#         if h.GetMaximum():
#             zvalues.append(h.GetBinContent(ibinx,ibiny)/h.GetMaximum() )
#         else:
#             zvalues.append(0 )

#         # print (h.GetYaxis().GetBinCenter(ibiny))

points = my_data[:,0:2]
# print(points)

def lifetimeToCoupling(lifetime_ns,msq):
    L_cm = lifetime_ns*29.98#cm/ns
    lamsq = (0.9/L_cm)*np.power(msq/100,4)*np.power(1/200,5)
    return np.sqrt(lamsq)

    # From my review paper
    # lamsq = (1/(10*lifetime_ns)) * np.power(msq/750,4)*np.power(1/2.,5)*np.power(10e-5,2)
    # return np.sqrt(lamsq)


for point in points:
    print(point)
    point[0],point[1] = point[1],point[0]
    point[0]*=0.001
    # convert lifetime to coupling strength
    # point[0] = lifetimeToCoupling(point[0],point[1])
    # print(point)
    point[0] = math.log10(point[0])
    print(point)


print(points)

zvalues = my_data[:,2]
print(zvalues)

# grid_z1 = griddata(points, zvalues, (grid_x, grid_y), method='linear')
grid_z1 = griddata(points, zvalues, (grid_x, grid_y), method='cubic')

# image = plt.plot([point[0] for point in points],[point[1] for point in points],"o",ms=2)

xvalues = [point[0] for point in points]
yvalues = [point[1] for point in points]

heatmap = plt.pcolor(grid_x, grid_y, grid_z1,vmax=50,vmin=-1e-10,rasterized=True)
cbar = plt.colorbar(heatmap)
plt.scatter(xvalues,yvalues,10,zvalues,ec='k',vmax=50,vmin=-1e-10)

# image = plt.imshow(grid_z1.T, origin='lower', extent=plottingRange, vmin=0, vmax=1)
# image = plt.imshow(grid_z1, extent=plottingRange)

contours = plt.contour(grid_x, grid_y, grid_z1,levels=[contourlevel], colors='white')

plt.clabel(contours)

# contours_5 = plt.contour(grid_x, grid_y, grid_z1,levels=[5],extent=plottingRange, colors='white')
# plt.clabel(contours_5, inline=1, fontsize=10, fmt=r"$5\sigma$", inline_spacing=20, manual=[(1,1)])

# plt.xlim([min(xvalues),max(xvalues)])
# plt.ylim([min(yvalues),max(yvalues)])

plt.xlim([plottingRange[0],plottingRange[1]])
plt.ylim([plottingRange[2],plottingRange[3] ])

# plt.xlabel("Latency")
# plt.ylabel("Threshold [e]")
# cbar.set_label("Efficiency (w.r.t. maximum)")

# # plt.text([plottingRange[2],plottingRange[3] ])
# plt.text(0.5, 1.05, f'{itype}_{ichip}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)


fig.savefig(f"test.pdf")
plt.clf()


