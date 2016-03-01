#!/usr/bin/env python

# ariadne-pipeline.py -- Create, manage, and execute pipelines.
import os
import sys
import Pipeline
import ariadnetools

def printUsage():
	print("Usage: ariadne-pipeline <command> [arguments]\n")
	print("Where <command> is one of the following:")
	print("\tlist  \tList all pipelines.")
	print("\trun   \tRun a pipeline.")
	print("\tcreate\tDefine a new pipeline.")
	exit(1)

def doList():
	dirList=os.listdir(".")

	for entry in dirList:
		ext=ariadnetools.getExtension(entry)
		if ext==".pipeline":
			if ariadnetools.getDefType(entry)=="pipeline":
				print(ariadnetools.getDefName(entry))

	return

def doRun(paramList):
	# Parse the parameters list:
	for param in paramList:
		
	return

def printCreateHelp():
	print("Usage: ariadne-pipeline.py create --name=<name> [args]\n")
	print("Where [args] represents one or more of the following:")
	print("\t--dependencies=<comma separated list>")
	print("\t--

def doCreate(paramList):
	
	# Parse the parameters list:
	for param in paramList:
		if param[0]=="--dependencies":
		elif param[0]=="--numjobs":
		elif param[0]=="--clean":
		else:
			printCreateHelp()

	
	return

if len(sys.argv==1):
	printUsage()

action=sys.argv[1]

# Now make a list containing the rest of the parameters:
paramList=[]
for i in range(2, len(sys.argv), 1):
	splitList=sys.argv[i].split('=')

	# Ensure that it's always the right size:
	for j in range(0, 2-len(splitList), 1):
		splitList.insert("")

	paramList.insert((splitList[0], splitList[1]))

if action=="list":
	doList()
elif action=="run":
	doRun(paramList)
elif action=="create":
	doCreate(paramList)
else:
	print("Error: Unknown command.")
	printUsage()
