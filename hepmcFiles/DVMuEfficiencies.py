#!/usr/bin/env python

import pyhepmc_ng
import ROOT
ROOT.gROOT.SetBatch()
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from particle import Particle

#--- INFORMATION ON UNITS ---
#functions give MeV, want to graph in GeV
#functions give mm

adapter = pyhepmc_ng.ReaderAsciiHepMC2(filename="1TeV_200GeV_1ps.hepmc")

evt = pyhepmc_ng.GenEvent(
    momentum_unit=pyhepmc_ng.Units.MEV, length_unit=pyhepmc_ng.Units.MM)

decaytime = []
properdecaytime = []
MET = []
METacceptance = []
muonAcc = []
CHARGED_PION_MASS = 139.570 #MeV

def fit_function(x, A, B):
	return (A * np.exp(-x/B))

def isCharged(particle):
	part = Particle.from_pdgid(particle.pid)
	if part.charge != 0: return 1
	else: return 0

def isReconstructable(particle):
	decay_dist = np.array([particle.end_vertex.position[0] - particle.production_vertex.position[0], particle.end_vertex.position[1] - particle.production_vertex.position[1], particle.end_vertex.position[2] - particle.production_vertex.position[2]])
	trans_decay_dist = np.sqrt(decay_dist[0]**2 + decay_dist[1]**2)
	if trans_decay_dist > 1:
		return True
	else:
		return False

def get_reconstructable_children(particle):
	for child in particle.children:
		decay_dist = np.array([child.end_vertex.position[0] - child.production_vertex.position[0], child.end_vertex.position[1] - child.production_vertex.position[1], child.end_vertex.position[2] - child.production_vertex.position[2]])
		trans_decay_dist = np.sqrt(decay_dist[0]**2 + decay_dist[1]**2)
		if trans_decay_dist > 1:
			return child
		else: 
			for ch in child.children:
				decay_dist = np.array([ch.end_vertex.position[0] - ch.production_vertex.position[0], ch.end_vertex.position[1] - ch.production_vertex.position[1], ch.end_vertex.position[2] - ch.production_vertex.position[2]])
				trans_decay_dist = np.sqrt(decay_dist[0]**2 + decay_dist[1]**2)
				if trans_decay_dist > 1: #placeholder value
					return ch

outputFile = ROOT.TFile("output.root","RECREATE")
h = {}
h = {}
h["MET"] = ROOT.TH1F("MET", "MET; MET [GeV]; events", 50, 0, 1000)
h["METacceptance"] = ROOT.TH1F("METacceptance", "MET acceptance; MET [GeV]; events", 50, 0, 1000)

for i in range(10):
	adapter.read_event(evt)
	if i%100 == 0:	
		print(i)

	sumInvisible = ROOT.TLorentzVector()
	muonEvtAcc = []
	passedMuEvtAcc = False
	passedMETacc = False
	passedVertexAcc = False

	for iparticle in evt.particles:
		if abs(iparticle.pid) in [12, 13, 14, 16]: #including muons in MET
			p = ROOT.TLorentzVector(iparticle.momentum.px, iparticle.momentum.py, iparticle.momentum.pz, iparticle.momentum.e)
			sumInvisible += p
			#add in LLP treatment
		if iparticle.pid == 1000022 and not iparticle.end_vertex.position: #first neutralino's end vertex is (0,0,0,0)? and that's messing up the following code, so I put the not part? seemed to work, so I assume that means null 
			#print(dir(iparticle))
			decaytime.append(iparticle.end_vertex.position[3])
			properdecaytime.append(iparticle.end_vertex.position[3]/(iparticle.momentum.e/iparticle.momentum.m()))
			selectedDecayProds = []
			sumSelDecayProds = ROOT.TLorentzVector()
			for ipart in get_reconstructable_children(iparticle):
				if isCharged(ipart) != 0 and ipart.momentum.pt/abs(ipart.charge) > 1000:
					selectedDecayProds.append(ipart)
					ipart_momentum = ROOT.TLorentzVector(ipart.momentum.px, ipart.momentum.py, ipart.momentum.pz, ipart.momentum.e)

					ipart_momentum.SetXYZM(ipart_momentum.Px(), ipart_momentum.Py(), ipart_momentum.Pz(),CHARGED_PION_MASS)
					sumSelDecayProds += ipart_momentum

			endvertex_x = iparticle.end_vertex.position[0]
			endvertex_y = iparticle.end_vertex.position[1]
			transverseDistance = sqrt(endvertex_x**2 + endvertex_y**2)
			numSelDecay = len(selectedDecayProds)
			InvMass = sumSelDecayProds.M()

			if transverseDistance > 4 and transverseDistance < 300 and abs(iparticle.end_vertex.position[2]) < 300 and numSelDecay >= 3 and InvMass > 20000:
				passedVertexAcc = True 
			#look at end vertex and find particles coming out of vertex (look into children function and find a way to loop over
			#make sure children are charged and have pt greater than 1GeV and then add to array of decay products
			# do the other checks about distance and stuff and then ask if there's more than 3 (selected) decay products from that end vertex
			# add 4 vec of selected decay products and then find invariant mass of sum and make sure it's larger than 20 GeV
				#rebuild 4 p that has same 3 p of sum and then assume pion mass instead of original mass for 4th comp
				#create TLorentz vec of decay prods and then use setM method to set it to pion mass
				#use this 4vec to find invariant mass
		if iparticle.pid == 13:
			rx = iparticle.production_vertex.position[0]
			ry = iparticle.production_vertex.position[1]
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

	if sumInvisible.Pt() > 100000: 
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
data_entries, bins = np.histogram(properdecaytime, bins=bins)

binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
popt, pcov = curve_fit(fit_function, xdata=binscenters[2:], ydata=data_entries[2:], p0=[100, .005])
#print(popt)
xspace = np.linspace(0, 0.04, 100000)

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

ax.bar(binscenters, data_entries, width=bins[1]-bins[0])
ax.plot(xspace, fit_function(xspace, *popt))
ax.set_yscale('log')
plt.xlabel("decay time")
plt.ylabel("entries")
plt.savefig("1TeV_200GeV_100ps_decaytime.pdf")
