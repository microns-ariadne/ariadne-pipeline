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

def printRunHelp():
	print("Usage: ariadne-pipeline run <pipeline> [arguments]\n")
	print("Where <pipeline> is the name of a pipeline in the")
	print("current working directory and [arguments] are any arguments")
	print("that have been defined in the top level module.")
	print("\nExample: ariadne-pipeline run testpipe -a=5")
	exit(1)

def doRun(paramList):
	if len(paramList)==0:
		printRunHelp()

	execArgs=[]
	pipeName=""

	# Parse the parameters list:
	for param in paramList:
		if param[0]=="--help":
			printRunHelp()
		elif param[0][0]=="-":
			execArgs.append(param[1])
		else:
			pipeName=param[0]

	p=Pipeline.Pipeline(pipeName+".pipeline")

	# Strip all of the names off of the args list for now:
	#finalArgs=[]
	#for e in execArgs:
#		if e[1]!="":
#			finalArgs.append(e)

	p.executePipe(execArgs)

def doInteractiveCreate():
	o=sys.stdout
	i=sys.stdin
	stageArgs=[]
	stages=[]
	topName=""
	
	o.write("Pipeline name: ")
	name=i.readline().strip()
	
	
	stagesExist=0
	while not stagesExist:
		print("Note: do not enter the highest level stage at this time.")
		o.write("Comma-separated list of stages (each must exist): ")
		stages=i.readline().strip().split(',')

		# Trim any blanks from the input list:
		ariadnetools.trimBlankStrings(stages)

		# If it's effecively empty (just a single-stage pipeline):
		if len(stages)==0:
			break

		stagesExist=1
		breakStage=""
		for s in stages:
			stagesExist=stagesExist and ariadnetools.fileExists(s, [".def",".stage"])
			if not stagesExist:
				breakStage=s
				break

		if not stagesExist:
			o.write("Stage: "+breakStage+" does not exist.\n")

	fileExists=0
	while not fileExists:
		o.write("Top pipeline stage (must exist): ")
		topName=i.readline().strip()
		fileExists=ariadnetools.fileExists(topName, [".def", ".stage"])

		if not fileExists:
			o.write("File doesn't exist.\n")

	# Try to load the top level module:
	topStage=None
	
	if ariadnetools.fileExists(topName+".def"):
		topStage=Pipeline.Stage(topName+".def")
	else:
		topStage=Pipeline.Stage(topName+".stage")

	# Commented out because all of the following will be useful when actually running the pipeline.
	#numTopStageArgs=topStage.numArgs()
	#argsMatch=0
	#while not argsMatch:
	#	o.write("Stage arguments. Should be a comma-separated list: ")
	#	stageArgs=i.readline().strip().split(',')

		# Now check if the args match up:
	#	if len(stageArgs)!=numTopStageArgs:
	#		print("Number of arguments ("+`len(stageArgs)`+" vs "+`numTopStageArgs`+") does not match")
	#	else:
	#		argsMatch=1

	p=Pipeline.Pipeline()
	p.name=name
	p.stageNames=stages
	p.topStage=topStage
	
	print("Writing pipeline definition file...")
	p.writeFile(name+".pipeline")
	print("Done.")


def printCreateHelp():
	print("Creates a pipeline definition file.")
	print("Usage: ariadne-pipeline create --name=<name> [args]\n")
	print("Where [args] represents one or more of the following:")
	print("\t--arguments=<comma separated list>")
	print("\t--stages=<list of stages in order of execution>")
	print("\t--topstage=<topmost execution stage>")
	print("\t--interactive")
	print("\nExample: ariadne-pipeline create --name=test --topstage=my_module --stages=mod1,mod2")
	exit(1)

def doCreate(paramList):
	if len(paramList)==0:
		printCreateHelp()
	
	# Parse the parameters list:
	stageArgs=[]
	stages=[]
	topName=""
	name=""
	runInteractive=0
	
	for param in paramList:
		if param[0]=="--arguments":
			stageArgs=param[1:]
		elif param[0]=="--stages":
			stages=param[1].split(',')
			ariadnetools.trimBlankStrings(stages)
		elif param[0]=="--topstage":
			topName=param[1]
		elif param[0]=="--interactive":
			runInteractive=1
		elif param[0]=="--name":
			name=param[1]
		else:
			printCreateHelp()

	if runInteractive:
		doInteractiveCreate()
	else:
		p=Pipeline.Pipeline()
		p.name=name
		p.stageNames=stages
		if ariadnetools.fileExists(topName+".stage"):
			p.topStage=Pipeline.Stage(topname+".stage")
		elif ariadnetools.fileExists(topName+".def"):
			p.topStage=Pipeline.Stage(topName+".def")
		else:
			print("Error: top stage does not exist! Please define and try again.")
			exit(2)

		if name=="":
			print("Error: need to specify a name for the pipeline.")
			exit(2)

		p.writeFile(name+".pipeline")

if len(sys.argv)==1:
	printUsage()

action=sys.argv[1]

# Now make a list containing the rest of the parameters:
paramList=[]
for i in range(2, len(sys.argv), 1):
	splitList=sys.argv[i].split('=')

	# Ensure that it's always the right size:
	for j in range(0, 2-len(splitList), 1):
		splitList.append("")

	paramList.append([splitList[0], splitList[1]])

if action=="list":
	doList()
elif action=="run":
	doRun(paramList)
elif action=="create":
	doCreate(paramList)
else:
	print("Error: Unknown command.")
	printUsage()
