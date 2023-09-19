#!/usr/bin/env python3

import ROOT
import numpy as np
import os
import sys

mass = str(sys.argv[1])
SR = str(sys.argv[2])

C = ROOT.TCanvas("C", "C", 800, 600)
i = 0

for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	seperatedStrings = filename.split('_')
	stopMass = seperatedStrings[1] #GeV
	lifetime = seperatedStrings[3] #ps
	if stopMass == mass:
		i += 1
		cutFlowFile = ROOT.TFile("cutflowFiles/%s"%filename)
		nrmHist = cutFlowFile.Get("%s normalized cut-flow"%SR).Clone("nrmCutFlow%s"%lifetime)
		if i == 1: nrmHist.Draw("")
		else: nrmHist.Draw("same")


C.SaveAs("%sGeV_normHistStack.pdf"%mass)
