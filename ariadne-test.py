#!/usr/bin/env python

import Pipeline
import ariadnetools
import os
import sys

# ariadne-test.py -- Test the pipeline.

def printUsage():
	print("Usage: ariadne-test <pipelinename> [args]")
	print("Do automated testing on a pipeline.")
	print("\nWhere [args] may be one or more of the following:")
	print("\t--dataset\tTests the pipeline with the specified dataset.")
	exit(1)

def runTest(pipelineName, datasetName):
	if datasetName=="":
		
	return

if len(sys.argv)==1:
	printUsage()

pipeName=sys.argv[1]
datasetName=""

if len(sys.argv)>2:
	argToks=sys.argv[2].split('=')
	if argToks[0]=="--dataset":
		datasetName=argToks[1]
	else:
		print("Invalid parameter: "+argToks[0])
		printUsage()

runTest(pipename, datsetName)
