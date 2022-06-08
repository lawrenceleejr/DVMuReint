#!/usr/bin/env python

import pyhepmc_ng
import ROOT
ROOT.gROOT.SetBatch()
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

adapter = pyhepmc_ng.ReaderAsciiHepMC2(filename="1TeV_200GeV_1ps.hepmc")

evt = pyhepmc_ng.GenEvent(
    momentum_unit=pyhepmc_ng.Units.MEV, length_unit=pyhepmc_ng.Units.MM)

#hist = TH1F("hist", "Decay Time of Neutralino; Neutralino Decay Time; Events", 20, 0, 100e-12)
decaytime = []
properdecaytime = []
MET = []
METacceptance = []

def fit_function(x, A, B):
	return (A * np.exp(-x/B))

outputFile = ROOT.TFile("output.root","RECREATE")
h = {}
h1 = {}
h["MET"] = ROOT.TH1F("MET", "MET; MET [MeV]; events", 50, 0, 1000)
h1["METacceptance"] = ROOT.TH1F("METacceptance", "MET acceptance; MET [MeV]; events", 50, 0, 1000)

for i in range(10):
	adapter.read_event(evt)
	if i%100 == 0:	
		print(i)
	#print(adapter)
	print(i)
	sumInvisible = ROOT.TLorentzVector()
	for iparticle in evt.particles:
		if abs(iparticle.pid) in [12, 13, 14, 16]:
			#print(iparticle.momentum.px)
			p = ROOT.TLorentzVector(iparticle.momentum.px, iparticle.momentum.py, iparticle.momentum.pz, iparticle.momentum.e)
			#print(p.Phi())
			sumInvisible += p
			#print("SumInvisible = ", sumInvisible.Print())
			#add in LLP treatment
		if iparticle.pid == 1000022: 
			#print(iparticle.pid)
			#print(iparticle)
			#print(iparticle.mass)
			#evt.vertices[iparticle.end_vertex]
			#print(dir(iparticle))
			#print(iparticle.momentum)
			#print(dir(iparticle.momentum))
			decaytime.append(iparticle.end_vertex.position[3])
			properdecaytime.append(iparticle.end_vertex.position[3]/(iparticle.momentum.e/iparticle.momentum.m()))
			#print(iparticle.momentum.e/iparticle.momentum.m())
			#hist.fill(iparticle.end_vertex.position[3], 1)
			print(dir(iparticle))
		#if iparticle.pid == 13:
			
			#if iparticle.Pt() > 62 and 
	MET.append(sumInvisible.Pt())
	if sumInvisible.Pt() > 100:
		METacceptance.append(sumInvisible.Pt())
		h1["METacceptance"].Fill(sumInvisible.Pt()/1000.)
	h["MET"].Fill(sumInvisible.Pt()/1000.)
	#print(sumInvisible.Pt())

C = ROOT.TCanvas("C", "", 600, 600)
h["MET"].Draw()
C.SaveAs("MET.pdf")
outputFile.Write()
outputFile.Close()

C1 = ROOT.TCanvas("C1", "", 600, 600)
h1["METacceptance"].Draw()
C1.SaveAs("METacceptance.pdf")
outputFile.Write()
outputFile.Close()

bins = np.linspace(0,.04, 21)
METbins = np.linspace(0, 1000, 51)
data_entries, bins = np.histogram(properdecaytime, bins=bins)

MET_entries, METbins = np.histogram(MET, bins=METbins)

binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
popt, pcov = curve_fit(fit_function, xdata=binscenters[2:], ydata=data_entries[2:], p0=[100, .005])
print(popt)
xspace = np.linspace(0, 0.04, 100000)

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

ax.bar(binscenters, data_entries, width=bins[1]-bins[0])
ax.plot(xspace, fit_function(xspace, *popt))
ax.set_yscale('log')
plt.xlabel("decay time")
plt.ylabel("entries")
plt.savefig("1TeV_200GeV_100ps_decaytime.pdf")

 
METfig = plt.figure()
METax = fig.add_subplot(1,1,1)
METax.bar(binscenters, MET_entries, width=METbins[1]-METbins[0])
plt.xlabel("MET value")
plt.ylabel("entries")
#plt.show()
plt.savefig("1TeV_200GeV_100ps_MET.pdf")		
