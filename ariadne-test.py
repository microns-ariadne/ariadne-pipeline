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
	if datasetName!="": #Attempt to fetch the dataset:
		os.system("ariadne-dataset.py fetch "+datasetName)
		
	p=Pipeline.Pipeline(pipelineName+".pipeline")

	if len(p.validationArgs)==0:
		print("Pipeline has no validation arguments.")
		print("Specify arguments and try again.")
		return
	p.executePipe(p.validationArgs)
	
	valid=p.validate()

	if valid==-1:
		print("Pipeline validation checks passed.")
	else:
		print("Pipeline validation failed on stage: "+p.stages[valid].name)

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

runTest(pipeName, datasetName)
