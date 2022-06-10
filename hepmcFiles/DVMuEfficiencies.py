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

decaytime = []
properdecaytime = []
MET = []
METacceptance = []
muonAcc = []

def fit_function(x, A, B):
	return (A * np.exp(-x/B))

outputFile = ROOT.TFile("output.root","RECREATE")
h = {}
h = {}
h["MET"] = ROOT.TH1F("MET", "MET; MET [MeV]; events", 50, 0, 1000)
h["METacceptance"] = ROOT.TH1F("METacceptance", "MET acceptance; MET [MeV]; events", 50, 0, 1000)

for i in range(10):
	adapter.read_event(evt)
	if i%100 == 0:	
		print(i)

	sumInvisible = ROOT.TLorentzVector()
	muonEvtAcc = []
	passedMuEvtAcc = False
	passedMETacc = False

	for iparticle in evt.particles:
		if abs(iparticle.pid) in [12, 13, 14, 16]:
			p = ROOT.TLorentzVector(iparticle.momentum.px, iparticle.momentum.py, iparticle.momentum.pz, iparticle.momentum.e)
			sumInvisible += p
			#add in LLP treatment
		if iparticle.pid == 1000022: 
			#print(dir(iparticle))
			decaytime.append(iparticle.end_vertex.position[3])
			properdecaytime.append(iparticle.end_vertex.position[3]/(iparticle.momentum.e/iparticle.momentum.m()))
			#look at end vertex and find particles coming out of vertex (look into children function and find a way to loop over
			#make sure children are charged and have pt greater than 1GeV and then add to array of decay products
			# do the other checks about distance and stuff and then ask if there's more than 3 (selected) decay products from that end vertex
			# add 4 vec of selected decay products and then find invariant mass of sum and make sure it's larger than 20 GeV
				#rebuild 4 p that has same 3 p of sum and then assume pion mass instead of original mass for 4th comp
				#create TLorentz vec of decay prods and then use setM method to set it to pion mass
				#use this 4vec to find invariant mass
		if iparticle.pid == 13:
			rx = iparticle.end_vertex.position[0]
			ry = iparticle.end_vertex.position[1]
			rvec = ROOT.TVector2(rx, ry)
			r_decay = rvec.Mod()
			pvec = ROOT.TVector2(iparticle.momentum.px, iparticle.momentum.py)
			d0 = r_decay*np.sin(rvec.DeltaPhi(pvec))
			if iparticle.momentum.pt() > 62 and abs(d0) > 2 and abs(d0) < 300 and iparticle.momentum.abs_eta() < 1.05:
				muonEvtAcc.append(iparticle)
			if iparticle.momentum.pt() > 25 and abs(d0) > 2 and abs(d0) < 300 and iparticle.momentum.abs_eta() < 2.5:
				muonAcc.append(iparticle)

	if len(muonEvtAcc) > 0:
		passedMuEvtAcc = True

	MET.append(sumInvisible.Pt())

	if sumInvisible.Pt() > 100:
		METacceptance.append(sumInvisible.Pt())
		h["METacceptance"].Fill(sumInvisible.Pt()/1000.)
	
	if len(METacceptance) > 0:
		passedMETacc = True
	
	h["MET"].Fill(sumInvisible.Pt()/1000.)

C = ROOT.TCanvas("C", "", 600, 600)
h["MET"].Draw()
C.SaveAs("MET.pdf")
outputFile.Write()

C1 = ROOT.TCanvas("C1", "", 600, 600)
h["METacceptance"].Draw()
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
plt.savefig("1TeV_200GeV_100ps_MET.pdf")		
