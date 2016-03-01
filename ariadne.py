#!/usr/bin/env python

# ariadne.py -- Central dispatcher for ariadne modules.

import os
import sys
import ariadnetools

def printUsage():
	print("Create, manage, and execute complex machine learning jobs.")
	print("Usage: ariadne <command> [<args>]")
	print("")
	print("Where <command> is one of the following:")
	print("\tdataset  \tFetch, list, or show dataset information.")
	print("\ttest     \tPerform a test.")
	print("\tbenchmark\tBenchmark the pipeline.")
	print("\tpipeline \tRun or get information about the pipeline.")
	return

def handleArgs(argsList):

	if len(argsList)==1:
		printUsage()
		exit(1)
	
	childArgs=[]
	childArgs.append("") #There must always be a dummy first arg.

	for i in range(2, len(argsList), 1):
		childArgs.append(argsList[i]);

	cmd=argsList[1]
	
	# Check to see if the command is invalid:
	if not (cmd=="dataset" or cmd=="test" or cmd=="benchmark" or cmd=="pipeline"):
		print("Error: unrecognized command.\n")
		printUsage()
		exit(1)

	retCode=os.spawnvp(os.P_WAIT, "ariadne-"+cmd+".py", childArgs)

	#if retCode!=0:
	#	print("Something bad has happened.");
	#else:
	#	print("It's good!");

handleArgs(sys.argv)
