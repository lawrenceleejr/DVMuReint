#!/usr/bin/env python

import ROOT
import numpy as np
import json
import os
import sys

xsFile = open('XSecData.json')
xsData = json.load(xsFile)

luminosity = 136 #fb^(-1)

SR = str(sys.argv[1]) #MET or Muon

#make file loop to loop over all MET and muon cutflow files of efficiencies script
for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	cutFlowFile = ROOT.TFile(filename)
	seperatedStrings = filename.split('_')
	stringList = []
	for i in range(len(seperatedStrings)):
		string = ""
		for j in seperatedStrings[i]:
			if j.isdigit(): 
				string += j
		stringList.append(string)
	stopMass = int(stringList[1]) #GeV
	neutralinoLifetime = int(stringList[2]) #ps 
	
	cutFlowHist = cutFlowFile.Get("%s cut-flow;1"%SR)

	numGeneratedEvts = cutFlowHist.GetBinContent(1)
	finalNumEvts = cutFlowHist.GetBinContent(4)
	crossSection = xsData["data"][str(stopMass)]["xsec_pb"]

	normalizedNumEvts = finalNumEvts*(luminosity*crossSection/numGeneratedEvts)
	print(normalizedNumEvts)

#name the output root file so that it contains the stop mass and neutralino lifetime in the program
#read in the root files loop over them and get the mass from the file name 
	#ask for the file names that match the expected structure and get a list of file names
	#you can parse the strings of file names to get the mass and lifetimes
#make looking at muon or met SR as a command line option

#the output should be a table (csv file) that has the expected number of events and the model parameters
