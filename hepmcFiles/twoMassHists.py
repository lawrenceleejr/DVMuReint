#!/usr/bin/env python3

import ROOT
import numpy as np
import os
import sys
#ROOT.gROOT.SetBatch()

mass1 = str(sys.argv[1])
mass2 = str(sys.argv[2])
SR = "MET"

C = ROOT.TCanvas("C", "C", 800, 600)
i = 0
hists = {}
lifetimes = [100,1000,10000]
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
legend = ROOT.TLegend(0.15, 0.15, 0.48,0.5)
legend.SetBorderSize(0)

#c100 = ROOT.TColor.GetFreeColorIndex()
#color100 = ROOT.TColor(c100, 0.23, 0.46, 0.69)
#color100.SetRGB(0.23, 0.46, 0.69)

for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	seperatedStrings = filename.split('_')
	stopMass = seperatedStrings[1] #GeV
	lifetime = int(seperatedStrings[3]) #ps
	masslifetime = stopMass+seperatedStrings[3]


	if lifetime in lifetimes:
		if stopMass == mass1 or stopMass == mass2:
			print("%s ps, %s GeV"%(lifetime,stopMass))
			i += 1
			cutFlowFile = ROOT.TFile("cutflowFiles/%s"%filename, "READ")
			ROOT.gROOT.cd()
			hists[masslifetime] = cutFlowFile.Get("%s normalized cut-flow"%SR).Clone("nrmCutFlow%s"%lifetime)
			hists[masslifetime].SetLineWidth(3)
			hists[masslifetime].GetXaxis().SetNdivisions(4)

			if stopMass == mass1:
				hists[masslifetime].SetLineColor(ROOT.TColor.GetColor('#3B76AF'))
				hists[masslifetime].SetMaximum(1500)
			if stopMass == mass2:
				hists[masslifetime].SetLineColor(ROOT.TColor.GetColor('#59A94A'))
				#hists[masslifetime].SetLineStyle(2)
 
			if lifetime == 100:
				hists[masslifetime].SetLineStyle(1) 
				#hists[masslifetime].SetLineColor(ROOT.TColor.GetColor('#3B76AF'))
			if lifetime == 1000: 
				hists[masslifetime].SetLineStyle(2)
				#hists[masslifetime].SetLineColor(ROOT.TColor.GetColor('#59A94A'))
			if lifetime == 10000: 
				hists[masslifetime].SetLineStyle(3)
				#hists[masslifetime].SetLineColor(ROOT.TColor.GetColor('#9F80C4'))
			
			if i == 1: hists[masslifetime].Draw("hist")
			else: hists[masslifetime].Draw("hist same")

			print(hists[masslifetime].GetLineColor())

			legend.AddEntry(hists[masslifetime], "%s GeV, %s ps"%(stopMass,lifetime), "l")
			
#			if i == 1: hists[masslifetime].Draw("plc hist")
#			else: hists[masslifetime].Draw("plc hist same")
			


C.SetLogy()
legend.SetHeader("Stop mass, neutralino lifetime", "C")
legend.Draw()
C.SaveAs("massCutFlowPDFs/%sand%sGeV_normHistStack.pdf"%(mass1,mass2))
