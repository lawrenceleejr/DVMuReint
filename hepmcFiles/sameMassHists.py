#!/usr/bin/env python3

import ROOT
import numpy as np
import os
import sys
ROOT.gROOT.SetBatch()

mass = str(sys.argv[1])
SR = str(sys.argv[2])

C = ROOT.TCanvas("C", "C", 800, 600)
#ROOT.gStyle.SetPalette(106)
i = 0
hists = {}
lifetimes = [100,1000,10000]
#histStack = ROOT.THStack("hs", "%s GeV %s SR Normalized Cutflows"%(mass, SR))
ROOT.gStyle.SetPalette(109)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
legend = ROOT.TLegend(0.7, 0.7, 0.89,0.89)
legend.SetBorderSize(0)

for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	seperatedStrings = filename.split('_')
	stopMass = seperatedStrings[1] #GeV
	lifetime = int(seperatedStrings[3]) #ps
	
	if lifetime in lifetimes:
		if stopMass == mass:
			print("%s ps"%lifetime)
			i += 1
			cutFlowFile = ROOT.TFile("cutflowFiles/%s"%filename, "READ")
			ROOT.gROOT.cd()
			hists[lifetime] = cutFlowFile.Get("%s normalized cut-flow"%SR).Clone("nrmCutFlow%s"%lifetime)
			hists[lifetime].SetLineWidth(3)
			hists[lifetime].GetXaxis().SetNdivisions(4) 
			legend.AddEntry(hists[lifetime], "%s ps"%lifetime, "l")
			if i == 1: hists[lifetime].Draw("plc hist")
			else: hists[lifetime].Draw("plc hist same")
			
			if lifetime == 100:
				hists[lifetime].SetLineColor(432+1)
			if lifetime == 1000:
                                hists[lifetime].SetLineColor(616+1)
			if lifetime == 10000:
                                hists[lifetime].SetLineColor(600+2)			




#histStack.Draw("pfc nostack")
C.SetLogy()
legend.SetHeader("Lifetime", "C")
legend.Draw()
C.SaveAs("massCutFlowPDFs/%sGeV_normHistStack.pdf"%mass)
