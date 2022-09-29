#!/usr/bin/env python

import sys
import pyhepmc_ng
import ROOT
ROOT.gROOT.SetBatch()
import matplotlib.pyplot as plt
import numpy as np
from numpy import random
from scipy.optimize import curve_fit
from particle import Particle

#importing root files and extracting histograms for efficiency calculation
truthMETfile = ROOT.TFile("HEPData_truthMET.root")
truthMEThist = truthMETfile.Get("Auxiliary Figure 8a/Hist1D_y1")

MuEvtLvlfile = ROOT.TFile("HEPData_MuEvtLvl.root")
MuEvtLvlHist = MuEvtLvlfile.Get("Auxiliary Figure 8b/Hist2D_y1")

MuLvlfile = ROOT.TFile("HEPData_MuLvl.root")
MuLvlhist = MuLvlfile.Get("Auxiliary Figure 9/Hist2D_y1")

VertexLvlfile = ROOT.TFile("HEPData_vertexLvl.root")
VertexLvlhist = VertexLvlfile.Get("Auxiliary Figure 10a/Hist1D_y1")

VertexLvlMuonfile = ROOT.TFile("HEPData_vertexLvlWithMuon.root")
VertexLvlMuonhist = VertexLvlMuonfile.Get("Auxiliary Figure 10b/Hist1D_y1")

#--- INFORMATION ON UNITS ---
#functions give MeV, want to graph in GeV
#functions give mm

adapter = pyhepmc_ng.ReaderAsciiHepMC2(filename=str(sys.argv[1]))

fileName = str(sys.argv[1])
seperatedStrings = fileName.split('_')
stringList = []
for i in range(len(seperatedStrings)):
	string = ""
	for j in seperatedStrings[i]:
		if j.isdigit(): 
			string += j
	stringList.append(string)
stopMass = int(stringList[1]) #GeV
neutralinoMass = int(stringList[2]) #GeV
neutralinoLifetime = int(stringList[3]) #ps

evt = pyhepmc_ng.GenEvent(momentum_unit=pyhepmc_ng.Units.MEV, length_unit=pyhepmc_ng.Units.MM)

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

def getCharge(particle):
	#it doesn't matter if we consider the charges of SUSY particles because they shouldn't be reconstructable
	if abs(particle.pid) > 1000000: return 0
	else:
		part = Particle.from_pdgid(particle.pid)
		charge = part.charge
		return charge

def get_reconstructable_children(particle, refPos):
	reconstructables = set()
	for child in particle.children:
		if child.end_vertex:
			decay_dist = [child.end_vertex.position[0] - refPos[0], child.end_vertex.position[1] - refPos[1], child.end_vertex.position[2] - refPos[2]]
			decayDist_3D = np.sqrt(decay_dist[0]**2 + decay_dist[1]**2 + decay_dist[2]**2)
		else:
			decayDist_3D = 1e12
		if decayDist_3D > 1:
			if decayDist_3D > 100:
				reconstructables.add(child)
		else: 
			reconstructables = reconstructables.union(set(get_reconstructable_children(child, refPos)))
	reconstructables = list(reconstructables)
	return reconstructables

def get_d0(particle):
	rx = particle.production_vertex.position[0]
	ry = particle.production_vertex.position[1]
	rvec = ROOT.TVector2(rx, ry) 
	r_decay = rvec.Mod()
	pvec = ROOT.TVector2(particle.momentum.px, particle.momentum.py)
	d0 = r_decay*np.sin(rvec.DeltaPhi(pvec))
	return d0

#Instantiating histogram objects
cutflowName = "cutflow_" + str(stopMass) + "_GeV_" + str(neutralinoLifetime) + "_ps"
print(cutflowName)
outputFile = ROOT.TFile("output.root","RECREATE")
histogramFile = ROOT.TFile("cutflowFiles/%s.root"%cutflowName, "RECREATE") #put directory/ in front of filename so it outputs into directory of cut-flow files
h = {}
h = {}
h["MET"] = ROOT.TH1F("MET", "MET; MET [GeV]; events", 50, 0, 1000)
h["METacceptance"] = ROOT.TH1F("METacceptance", "MET acceptance; MET [GeV]; events", 50, 0, 1000)
h["Reconstructables"] = ROOT.TH1F("Reconstructable Decay Products", "Reconstructables; Number reconstructables; events", 50, 0, 100)
h["Selected decay prods"] = ROOT.TH1F("Selected Decay Products", "Selected decay prods; num selected decay prods; events", 50, 0, 100)
h["decay products"] = ROOT.TH1F("Decay products", "decay products; num decay products; events", 50, 0, 100)
h["proper decay time"] = ROOT.TH1F("proper decay time", "proper decay Time; decay time (mm); events", 50, 0, 30)
h["MET cut-flow"] = ROOT.TH1F("MET cut-flow", "MET cut-flow; cuts; events", 4, 0, 4)
h["Muon cut-flow"] = ROOT.TH1F("Muon cut-flow", "Muon cut-flow; cuts; events", 4, 0, 4)

passingEvents = 0
numEvents = 1000

#event loop
for i in range(numEvents):
	adapter.read_event(evt)
	if i%100 == 0 and i > 0:	
		print(i)

	sumInvisible = ROOT.TLorentzVector()
	muonEvtAcc = []
	passedMuEvtAcc = False
	passedMETacc = False
	passedVertexAcc = False
	passedMuAcc = False
	d0_array = []
	hasAttachedMuon = False
	vertexArr = []
	muonArr = []
	evtPassedMETeff = False
	evtPassedMuEff = False

	#particle loop
	for iparticle in evt.particles:
		#calculating MET
		if abs(iparticle.pid) in [12, 13, 14, 16]: #including muons in MET
			p = ROOT.TLorentzVector(iparticle.momentum.px, iparticle.momentum.py, iparticle.momentum.pz, iparticle.momentum.e)
			sumInvisible += p
			#add in LLP treatment

		if iparticle.pid == 1000022 and iparticle.end_vertex is not None: 
			#print(dir(iparticle))

			numdecayprod = len(iparticle.children)
			h["decay products"].Fill(numdecayprod)	
			
			#proper decay time of neutralino
			decaytime.append(iparticle.end_vertex.position[3])
			properdecaytime.append(iparticle.end_vertex.position[3]/(iparticle.momentum.e/iparticle.momentum.m()))
			h["proper decay time"].Fill(iparticle.end_vertex.position[3]/(iparticle.momentum.e/iparticle.momentum.m()))

			#vertex-level acceptance
			selectedDecayProds = []
			sumSelDecayProds = ROOT.TLorentzVector()
			
			#
			numReconstructables = len(get_reconstructable_children(iparticle, iparticle.end_vertex.position))
			h["Reconstructables"].Fill(numReconstructables)
			#
 
			#finding selected decay products
			for ipart in get_reconstructable_children(iparticle, iparticle.end_vertex.position):
				if getCharge(ipart) != 0 and ipart.momentum.pt()/abs(getCharge(ipart)) > 1000:
					selectedDecayProds.append(ipart)
					ipart_momentum = ROOT.TLorentzVector(ipart.momentum.px, ipart.momentum.py, ipart.momentum.pz, ipart.momentum.e)

					ipart_momentum.SetXYZM(ipart_momentum.Px(), ipart_momentum.Py(), ipart_momentum.Pz(),CHARGED_PION_MASS)
					sumSelDecayProds += ipart_momentum
				if ipart.pid == 13 and iparticle.momentum.pt() > 25000 and abs(get_d0(ipart)) > 2 and abs(get_d0(ipart)) < 300 and iparticle.momentum.abs_eta() < 2.5:
					hasAttachedMuon = True

			endvertex_x = iparticle.end_vertex.position[0]
			endvertex_y = iparticle.end_vertex.position[1]
			transverseDistance = np.sqrt(endvertex_x**2 + endvertex_y**2)
			numSelDecay = len(selectedDecayProds)
			InvMass = sumSelDecayProds.M()
			
			h["Selected decay prods"].Fill(numSelDecay)

			if transverseDistance > 4 and transverseDistance < 300 and abs(iparticle.end_vertex.position[2]) < 300 and numSelDecay >= 3 and InvMass > 20000:
				passedVertexAcc = True
				if hasAttachedMuon:
					MuonVertexEff = VertexLvlMuonhist.GetBinContent(VertexLvlMuonhist.FindBin(transverseDistance))
					randomNum = random.rand()
					if randomNum <= MuonVertexEff:
						vertexArr.append(iparticle.end_vertex.position)
				else:
					NoMuonVertexEff = VertexLvlhist.GetBinContent(VertexLvlhist.FindBin(transverseDistance))
					randomNum = random.rand()
					if randomNum <= NoMuonVertexEff:
						vertexArr.append(iparticle.end_vertex.position)

		if iparticle.pid == 13:
			#muon event level acceptance
			d0 = get_d0(iparticle)
			if iparticle.momentum.pt() > 62000 and abs(d0) > 2 and abs(d0) < 300 and iparticle.momentum.abs_eta() < 1.05:
				muonEvtAcc.append(iparticle)
				d0_array.append(abs(d0))
				

			#muon level acceptance
			if iparticle.momentum.pt() > 25000 and abs(d0) > 2 and abs(d0) < 300 and iparticle.momentum.abs_eta() < 2.5:
				muonAcc.append(iparticle)
				MuEff = MuLvlhist.GetBinContent(MuLvlhist.FindBin(abs(d0), iparticle.momentum.pt()/1000.))
				randomNum = random.rand()
				if randomNum <= MuEff: 
					muonArr.append(iparticle)

	if len(muonEvtAcc) > 0:
		passedMuEvtAcc = True
		MuEvtEff = MuEvtLvlHist.GetBinContent(MuEvtLvlHist.FindBin(min(d0_array), sumInvisible.Pt()/1000.))
		randomNum = random.rand()
		if randomNum <= MuEvtEff: evtPassedMuEff = True
	if len(muonAcc) > 0:
		passedMuAcc = True

	MET.append(sumInvisible.Pt())

	if sumInvisible.Pt() > 100000: 
		METacceptance.append(sumInvisible.Pt())
		h["METacceptance"].Fill(sumInvisible.Pt()/1000.)
		truthMETefficiency = truthMEThist.GetBinContent(truthMEThist.FindBin(sumInvisible.Pt()/1000.))
		randomNum = random.rand()
		if randomNum <= truthMETefficiency: evtPassedMETeff = True
		
	if len(METacceptance) > 0:
		passedMETacc = True
	

	h["MET"].Fill(sumInvisible.Pt()/1000.)
	
	h["MET cut-flow"].Fill(0)
	h["Muon cut-flow"].Fill(0)
	
	if evtPassedMETeff: 
		h["MET cut-flow"].Fill(1)
	if evtPassedMuEff:
		h["Muon cut-flow"].Fill(1)
	if len(vertexArr) == 0:
		continue 
	h["MET cut-flow"].Fill(2)
	h["Muon cut-flow"].Fill(2)
	if len(muonArr) == 0:
		continue
	h["MET cut-flow"].Fill(3)
	h["Muon cut-flow"].Fill(3)
	#store histogram in root file and use a different script to get the number of events in this last bin
	#take this number of events and multiply it by (luminosity*cross section)/number of events in first bin
		#compare this number to the one in the table to see if it's excluded
	#luminosity is from the paper (136 fb^-1)
	#cross section is from the SUSY cross section twiki for stops (function of stop mass)
		#use the look up table and gitHub link to find the cross section
	#output masses and lifetime and num events and output of calculation above in table
	#if 3 is filled, then you've gotten through to MET signal region
	
C = ROOT.TCanvas("C", "", 600, 600)
h["MET"].Draw()
C.SaveAs("MET.pdf")
outputFile.Write()

C1 = ROOT.TCanvas("C1", "", 600, 600)
h["METacceptance"].Draw()
C1.SaveAs("METacceptance.pdf")
outputFile.Write()

C2 = ROOT.TCanvas("C2", "", 600, 600)
h["Reconstructables"].Draw()
C2.SaveAs("Reconstructables.pdf")

C3 = ROOT.TCanvas("C3", "", 600, 600)
h["Selected decay prods"].Draw()
C3.SaveAs("Selected_decay_products.pdf")

C4 = ROOT.TCanvas("C4", "", 600, 600)
h["decay products"].Draw()
C4.SaveAs("decay_products.pdf")

C5 = ROOT.TCanvas("C5", "", 600, 600)
h["proper decay time"].Draw()
C5.SaveAs("rawproperdecaytime.pdf")

C6 = ROOT.TCanvas("C6", "", 600, 600)
h["MET cut-flow"].Draw()
C6.SaveAs("METcutFlow.pdf")

C7 = ROOT.TCanvas("C7", "", 600, 600)
h["Muon cut-flow"].Draw()
C7.SaveAs("MuonCutFlow.pdf")
outputFile.Close()

histogramFile.WriteObject(h["MET cut-flow"], "MET cut-flow")
histogramFile.WriteObject(h["Muon cut-flow"], "Muon cut-flow")
histogramFile.Close()

### Alexander's Playground #####
#file = ROOT.TFile.Open("cutflowFiles/%s.root"%cutflowName, "READ")


###############################
bins = np.linspace(0, 3., 31)
data_entries, bins = np.histogram(properdecaytime, bins=bins)

binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
popt, pcov = curve_fit(fit_function, xdata=binscenters[2:], ydata=data_entries[2:], p0=[2500, 0.3])
#print(popt)
xspace = np.linspace(0, 3., 100000)

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

ax.bar(binscenters, data_entries, width=bins[1]-bins[0])
ax.plot(xspace, fit_function(xspace, *popt), color="orange", label="fit: a=%5.3f, b=%5.3f" % tuple(popt))
ax.set_yscale('log')
plt.xlabel("decay time")
plt.ylabel("entries")
plt.legend()
plt.title("Proper decay time of neutralino")
plt.savefig("properdecaytime.pdf")


