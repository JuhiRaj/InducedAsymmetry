
################################################################################
#### This Script Inputs two histograms - Experimental Data and Raw MC Data #####
#### The Script then minimizes the chi square function using TMinuit to estimate the induced asymmetry ####
################################################################################

import argparse
from ROOT import *
from ROOT import TMinuit , Double , Long
import numpy as np
from array import array as arr
from os import listdir, system
from fnmatch import filter
import sys
import os
import math



#The parser sets the input parameters for the script to run#
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--input_data", required=True, type=str,help="Path to the .root file created by the output of j-pet-framework-examples from experimental data")
parser.add_argument("-m", "--input_mc", required=True, type=str,help="Path to the .root file created by the output of j-pet-framework-examples from MC data")
args = vars(parser.parse_args())


def main():
#The first part of the script is to input the root files#

	canvas = TCanvas("Canvas_d", "Canvas_d", 533, 76, 1383, 852)
	input_datafile = TFile(args["input_data"])
	EV_data = input_datafile.Get("EventCategorizer subtask 0 stats/ExpecValue")
	entries_data = EV_data.GetSize()	
	print "# of Entries in Data file:",entries_data 
	print "Experimental Data Inputed"
	data_arr = []

	canvas = TCanvas("Canvas_mc", "Canvas_mc", 533, 76, 1383, 852)
	input_mcfile = TFile(args["input_mc"])
	EV_mc = input_mcfile.Get("EventCategorizer subtask 0 stats/ExpecValue_Smeared")
	entries_mc = EV_mc.GetSize()	
	print "# of Entries in MC file:",entries_mc
	print "MC Data Inputed"
	mc_arr = []
	bin_arr = []

	for x in range(entries_data):
		Data_i = EV_data.GetBinContent(x)	
		MC_i = EV_mc.GetBinContent(x)
		data_arr.append(Data_i)
		mc_arr.append(MC_i)	
		Bin_i = EV_data.GetBinCenter(x)
		bin_arr.append(Bin_i)		
		#print Data_i 
		#print MC_i
	
	#print data_arr
	#print mc_arr
	#print bin_arr

# --> Set parameters and function to f i t
	name = ["c","d"] #variable names
	vstart = arr('d',(1.0,1.0)) #the initial values
	step = arr('d',(0.001,0.001)) #the initial step size
	npar = len(name)

# --> Defining the Chi-Square function to be minimized#
	
	def Chi_Induced(Data, MC, BinCenter, C, D):
		chi = 0.
		for i in range(0,entries_data):
			#num1 = Data[i]
			#num2 = D*((1-(C*BinCenter[i]))*MC[i])
			#num = (num1 - num2)**2
			#num = 0.			
			#den1 = ((Data[i])**(1/2))**2
			#den2 = (D*((1-(C*BinCenter[i])))*((MC[i])**(1/2)))**2
			num = 2
			den = 2
			#den = den1 + den2
			chi = chi + num/den
		return chi
	
	
# --> set up MINUIT
	myMinuit = TMinuit(npar) # initialize TMinuit with maximum of npar parameters
	myMinuit.SetFCN(Chi_Induced) # set function to minimize
	ierflg = Long(0)
	arglist = arr('d', 2*[0.01]) # set error definition 	
	arglist [0] = 6000 # Number of calls for FCN before gving up
	arglist [1] = 0.3 # Toleranceierflg = Long(0)
	myMinuit.mnexcm("SET ERR",arglist,1,ierflg)
	for i in range(0,npar):
		myMinuit.mnparm(i, name[i] , vstart[i], step[i], 0, 0, ierflg)
	myMinuit.mnexcm("MIGRAD", arglist ,1,ierflg) # execute the minimisation
	# --> check TMinuit status
	amin , edm , errdef = Double (0.) , Double (0.) , Double (0.)
	nvpar , nparx , icstat = Long (0) , Long (0) , Long (0)
	myMinuit.mnstat ( amin , edm , errdef , nvpar , nparx , icstat )


	#EV_data.Draw()
	#canvas.SaveAs("EV_data.png")





main()
