#!/usr/bin/env python

import os,sys
# import ROOT
import numpy as np
import scipy
from scipy.interpolate import griddata
from scipy import signal
import matplotlib.pyplot as plt
import math
import seaborn as sns


# f = ROOT.TFile("outputPlots_220822.root")

from numpy import genfromtxt
my_data = genfromtxt('MET_normalized_num_evts.csv', delimiter=',',skip_header=1)

# print(my_data)

plottingRange = (-5,-1,400,2000)
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
    # lamsq = (0.9/L_cm)*np.power(msq/100,4)*np.power(1/200,5)
    lamsq = 550*(0.9/L_cm)*np.power(msq/100,4)*np.power(1/200,5)
    return np.sqrt(lamsq)

    # From my review paper
    # lamsq = (1/(10*lifetime_ns)) * np.power(msq/750,4)*np.power(1/2.,5)*np.power(10e-5,2)
    # return np.sqrt(lamsq)


def couplingToLifetime(coupling,msq):
    lamsq = np.power(coupling,2)
    L_cm = 550*(0.9/lamsq)*np.power(msq/100,4)*np.power(1/200,5)
    return L_cm/29.98

for point in points:
    tmplifetime = point[1]
    # print(point)
    point[0],point[1] = point[1],point[0]
    point[0]*=0.001
    # convert lifetime to coupling strength
    point[0] = lifetimeToCoupling(point[0],point[1])
    if tmplifetime==10:
        print(point,tmplifetime)
    # print(point)
    point[0] = math.log10(point[0])
    # print(point)


# print(points)

zvalues = my_data[:,2]
# print(zvalues)

# grid_z1 = griddata(points, zvalues, (grid_x, grid_y), method='linear')
# grid_z1 = griddata(points, zvalues, (grid_x, grid_y), method='cubic')



#### RBF test

xArray = points[:,0]
yArray = points[:,1]

yScaling = (np.max(xArray)-np.min(xArray))/(np.max(yArray)-np.min(yArray)) if np.max(yArray) else 1
yArray = yArray*yScaling


# RBF

rbf = scipy.interpolate.Rbf(xArray, yArray, zvalues, function="multiquadric", smooth=0.5 , epsilon=0.5)

xlinspace = np.linspace(xArray.min(),
                        xArray.max(),
                        200)
ylinspace = np.linspace(yArray.min(),
                        yArray.max(),
                        200)

xymeshgrid = np.meshgrid(xlinspace,ylinspace)

grid_z1 = rbf(xymeshgrid[0], xymeshgrid[1])


# griddata

# grid_z1 = scipy.interpolate.griddata( (xArray,yArray), zvalues, (xymeshgrid[0], xymeshgrid[1]), method="cubic" )




xymeshgrid[1] = xymeshgrid[1] / yScaling
yArray = yArray/yScaling

grid_x = xymeshgrid[0]
grid_y = xymeshgrid[1]



########################


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


# print(len(contours.collections[0].get_paths()))
p = contours.collections[0].get_paths()[0]
v1 = p.vertices

try:
    p = contours.collections[0].get_paths()[1]
    v2 = p.vertices
    v = np.concatenate((v1,v2))
except:
    v = v1
    pass

v = v[160:]
# v = v[54:]
# v = v[95:]

x = v[:,0]
y = v[:,1]

x = np.power(10,x)

thiswork_x = x
thiswork_y = y

############## PLOT STUFF #####################

fig, ax = plt.subplots()




for lifetime in [0.001,0.01,0.1,1,10,100]:
    masses = np.array(range(400,1700,10))
    couplings = lifetimeToCoupling(lifetime,masses)
    plt.plot(couplings,masses,":",c="grey",lw=1,alpha=0.3)
    plt.text(lifetimeToCoupling(lifetime,1350)*0.75,1350,r"$\tau=10^{%d}$ ns"%(np.log10(lifetime)),rotation=75, alpha=0.3,size=9)






# RPC 0L

rpc0l = genfromtxt('RPC0L.csv', delimiter=',',skip_header=0)
plt.plot(rpc0l[:,0],rpc0l[:,1],c="tab:blue",lw=3,alpha=0.3)
plt.text(1.0e-4,430,"ATLAS RPC Stop 0L\n"+r"36.1 fb$^{-1}$",size=9,c="tab:blue",ha="left",alpha=0.7,weight='bold')



# RPV 1L

rpv1l = genfromtxt('RPV1L.csv', delimiter=',',skip_header=0)
rpv1l = rpv1l[10:-20]
plt.plot(rpv1l[:,0],rpv1l[:,1],c="tab:green",lw=3,alpha=0.3)
plt.text(2.0e-3,750,"ATLAS RPV 1L\n"+r"36.1 fb$^{-1}$",size=9,c="tab:green",ha="left",alpha=0.7,weight='bold')








# THIS WORK



def doFillBetween(x,y,n=100,dy=0.995,color="k",alpha=0.6,log=True,axis=ax):
    initialY = y
    tmpy = initialY

    colorpal = sns.light_palette(color, n)[::-1]
    for i in range(n):
        if log:
            axis.fill_between(x,tmpy, [thing*dy for thing in tmpy],linewidth=0,color=colorpal[i],alpha = alpha*((n-i)/float(n) ) ,rasterized=True)
            tmpy = [thing*dy for thing in tmpy]



# mycolor = "k"
mycolor = "tab:orange"

doFillBetween(thiswork_x,thiswork_y,color=mycolor)
plt.plot(thiswork_x[1:-1],thiswork_y[1:-1],"-",c=mycolor,lw=1)

labelIndex = 200

plt.text(thiswork_x[labelIndex]*0.8,thiswork_y[labelIndex],"ATLAS DV+mu\n"+r"136 fb$^{-1}$"+"\n(This work)",size=12,c=mycolor,weight='bold',ha="right")


ax.set_xlabel(r"$\lambda''_{323}$")
ax.set_ylabel(r"$m(\tilde{t})$ [GeV]")

ax.set_xscale('log')


plt.xlim([5e-5,5e-2])
plt.ylim([400,1600])

fig.savefig("contourplot.pdf")















