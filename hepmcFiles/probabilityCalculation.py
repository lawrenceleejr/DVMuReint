#!/usr/bin/env python

import ROOT
import numpy as np
import json
import os
import sys
import csv

xsFile = open('XSecData.json')
xsData = json.load(xsFile)

neutralinoLifetime = 0

luminosity = 136*1000 #pb^(-1)

SR = str(sys.argv[1]) #MET or Muon

f = open("normalized_num_evts.csv", "w")
writer = csv.writer(f)
header = ["mass", "lifetime", "normalizedNumEvts"]
writer.writerow(header)

#make file loop to loop over all MET and muon cutflow files of efficiencies script
for ifile in os.listdir("cutflowFiles"):
	filename = os.fsdecode(ifile)
	cutFlowFile = ROOT.TFile("cutflowFiles/%s"%filename, "UPDATE")
	seperatedStrings = filename.split('_')
	#stringList = []
	#for i in range(len(seperatedStrings)):
	#	string = ""
	#	for j in seperatedStrings[i]:
	#		if j.isdigit(): 
	#			string += j
	#	stringList.append(string)
	stopMass = int(seperatedStrings[1]) #GeV
	neutralinoLifetime = int(seperatedStrings[3]) #ps 
	cutFlowFile.ls()
	print( "%s cut-flow"%SR)	
	cutFlowHist = cutFlowFile.Get("%s cut-flow"%SR)
	numGeneratedEvts = cutFlowHist.GetBinContent(1)
	finalNumEvts = cutFlowHist.GetBinContent(4)
	crossSection = xsData["data"][str(stopMass)]["xsec_pb"] #pb
	normCutFlowHist = cutFlowHist.Clone("%s normalized cut-flow"%SR)
	normCutFlowHist.Scale(luminosity*crossSection/numGeneratedEvts)
	normCutFlowHist.Write()
	
	normalizedNumEvts = finalNumEvts*(luminosity*crossSection/numGeneratedEvts)
	
	data = [stopMass, neutralinoLifetime, normalizedNumEvts]
	writer.writerow(data)

	print(normalizedNumEvts)
	print(f"{normalizedNumEvts=}")
	print(f"{finalNumEvts=}")
	print(f"{luminosity=}")
	print(f"{crossSection=}")
	print(f"{numGeneratedEvts=}")

cutFlowFile.Write()
#name the output root file so that it contains the stop mass and neutralino lifetime in the program
#read in the root files loop over them and get the mass from the file name 
	#ask for the file names that match the expected structure and get a list of file names
	#you can parse the strings of file names to get the mass and lifetimes
#make looking at muon or met SR as a command line option

#the output should be a table (csv file) that has the expected number of events and the model parameters
