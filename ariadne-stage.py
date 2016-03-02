#!/usr/bin/env python

# ariadne-stage.py -- Allows stage testing and specification

import os
import sys
import ariadnetools
import Pipeline

def printUsage():
	print("Usage: ariadne-stage <command> [args]")
	print("Manage, test, and compile individual pipeline stages.")
	print("\nWhere <command> is one of the following:")
	print("\tcreate\tCreates a new stage definition.")
	print("\tshow  \tDisplays information about a stage.")
	print("\tcompile\tCompiles the stage into a luigi module.")
	print("\trun   \tAttempts to execute the stage.")
	exit(1)

def printCreateHelp():
	print("Usage: ariadne-stage create --name=<name> [args]")
	print("Create a pipeline stage definition file.")
	print("Where [args] may be one or more of the following:")
	print("\t--interactive")
	print("\t--pysource=<file>")
	print("\t--commands=<comma separated list of commands>")
	print("\t--arguments=<comma separated list of arguments and their types.>")
	print("\t--dependencies=<comma separated list of dependencies.>")
	print("\t--output=<not yet used.>")
	exit(1)

def doCreateInteractive():
	i=sys.stdin
	o=sys.stdout

	s=Pipeline.Stage()

	o.write("Is this stage already defined in a python module (y/n)? ")
	resp=i.readline().strip()

	if resp=="y":
		o.write("Enter the module's name: ")
		resp=i.readline().strip()
		s.name=resp
		s.isDirectModule=1
		s.directModuleName=resp
		s.writeFile(resp+".stage")
		return

	
	print("Using module compilation model.")
	print("Enter the stage's name: \n")
	s.name=i.readline().strip()

	print("\nEnter arguments as a comma-separated list:")
	print("eg. A INT, B OTHER, C DATE\n")
	s.args=ariadnetools.striplist(i.readline().strip().split(','))

	print("\nEnter dependencies as a comma-separated list:")
	print("eg. foo(A), bar(B)\n")
	s.dependencies=ariadnetools.striplist(i.readline().strip().split(','))

	print("\nEnter commands as a comma-separated list:")
	print("eg. EXEC ls >C, NATIVE f=open(C)\n")
	s.commands=ariadnetools.striplist(i.readline().strip().split(','))

	print("Writing stage definition file...")
	s.writeFile(s.name+".stage")
	print("Done")
	return

def doCreate(args):
	sourceFile=""	
	cmdList=[]
	rawArgList=[]
	rawDependencies=[]
	output=""
	name=""

	for a in args:
		if a[0]=="--interactive":
			doCreateInteractive()
		elif a[0]=="--pysource":
			sourceFile=a[1]
		elif a[0]=="--commands":
			cmdList=ariadnetools.trimBlankStrings(a[1].split(','))
		elif a[0]=="--arguments":
			rawArgList=ariadnetools.trimBlankStrings(a[1].split(','))
		elif a[0]=="--dependencies":
			rawDependencies=ariadnetools.trimBlankStrings(a[1].split(','))
		elif a[0]=="--output":
			output=a[1]
		elif a[0]=="--name":
			name=a[1]

	s=Pipeline.Stage()
	if sourceFile=="":
		s.isDirectModule=1
		s.directModuleName=sourceFile
	s.name=name
	s.commands=cmdList
	s.dependencies=rawDependencies()
	s.arguments=rawArgList
	s.output.append(output)

	s.writeFile(name+".stage")
	
	return

def doShow(args):
	return

def doCompile(args):
	return

def doRun(args):
	return

if len(sys.argv)<2:
	printUsage()

# Now set up a command:
command=sys.argv[1]

args=ariadnetools.argPair(sys.argv, 2)

if command=="create":
	doCreate(args)
elif command=="show":
	doShow(args)
elif command="compile":
	doCompile(args)
elif command="run":
	doRun(args)
else:
	print("Invalid command: "+command)
	printUsage()
