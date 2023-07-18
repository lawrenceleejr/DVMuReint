#!/usr/bin/env python3

import ROOT
import numpy as np
import os
import sys

mass = str(sys.argv[1])
SR = str(sys.argv[2])
#nrmHists = ROOT.THStack("Normalized Histograms mass: %s"%mass, "Normalized Histograms mass: %s"%mass)

C = ROOT.TCanvas("C", "", 600, 600)

for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	seperatedStrings = filename.split('_')
	print(seperatedStrings[1])
	stopMass = int(seperatedStrings[1]) #GeV
	if stopMass == mass:
		cutFlowFile = ROOT.TFile("cutflowFiles/%s"%filename, "UPDATE")
		nrmHist = cutFlowFile.Get("%s normalized cut-flow"%SR)
		nrmHist.Draw()
#		nrmHists.Add(nrmHist)

#C = ROOT.TCanvas("C", "",10,10, 600, 600)
#nrmHists.Draw()
C.SaveAs("%sGeV_normHistStack.pdf"%mass)
