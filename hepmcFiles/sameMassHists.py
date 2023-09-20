#!/usr/bin/env python3

import ROOT
import numpy as np
import os
import sys
ROOT.gROOT.SetBatch()

mass = str(sys.argv[1])
SR = str(sys.argv[2])

C = ROOT.TCanvas("C", "C", 800, 600)
ROOT.gStyle.SetPalette(106)
i = 0
hists = {}
lifetimes = [100,1000,10000]

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
		#	print(ROOT.gDirectory.ls())
			print(hists[lifetime].GetBinContent(2))
			if i == 1: hists[lifetime].Draw("pfc hist")
			else: hists[lifetime].Draw("pfc hist same")

C.SetLogy()
C.SaveAs("%sGeV_normHistStack.pdf"%mass)
