#!/usr/bin/env python

# ariadne-dataset -- Ariadne module to fetch, manage, and unpack datasets.

import os
import sys
import DatasetDefs

import ariadnetools

def printUsage():
	print("Usage: ariadne-dataset <command> [args]")
	print("")
	print("Where <command> is one of the following:")
	print("\tfetch  \t Fetch a dataset specified by name.")
	print("\tlist   \t List all dataset files in the current directory.")
	print("\tcreate \t Creates a dataset definition file.")
	print("\tshow   \t Print information about a dataset.")
	exit(1)

def doFetch(dsname):
	d=DatasetDefs.Def(dsname+".def")

	pids=[]
	
	# Fire off download jobs:
	for u in d.urlList:
		pids.append((os.spawnlp(os.P_NOWAIT, "ariadne-download.sh", "ariadne-download.sh", u),ariadnetools.getUrlFilename(u)))

	print("Fetching datasets...")

	for p in pids:
		status=os.waitpid(p[0], 0)
		rcode=status[1]&0xFF00
		if rcode!=0:
			print("Couldn't download or exists: "+p[1])

	unpacks=[]

	print("Extracting datasets (if possible)...")

	# Now that we have all of the downloads, unpack them as appropriate:
	for p in pids:
		ext=ariadnetools.getExtension(p[1])
		
		# The unpack script should just fall through if the archive is unsupported:
		unpacks.append(os.spawnlp(os.P_NOWAIT, "ariadne-unpack.sh", "ariadne-unpack.sh", p[1], ext))

	for u in unpacks:
		os.waitpid(u, 0)
	return

def doList():
	curDir=os.listdir(".")

	for entry in curDir:
		ext=ariadnetools.getExtension(entry)
		if ext==".def":
			if ariadnetools.getDefType(entry)=="dataset":
				print(ariadnetools.getDefName(entry))
	
	return

def printCreateHelp():
	print("Usage: ariadne-dataset create --name=<datasetname> <URL method>\n")
	print("Where <URL method> is one of the following:")
	print("\t--dirlisting=<path>\tUse all files in the specified path.")
	print("\t--console          \tRead URLs from stdin.")
	print("\t--file=<file>      \tRead URLs from the specified file.")
	exit(1)
	
def doCreate():
	d=DatasetDefs.Def()

	print("Dataset name (--name)?")
 	d.datasetName=sys.stdin.readline().rstrip()
	
	inputMethod=""

	while not (inputMethod=="file" or inputMethod=="console" or inputMethod=="dirlisting"):
		print("Available URL list input methods: file, console, dirlisting")
		print("Input method?")
		inputMethod=sys.stdin.readline().rstrip()
	f=None

	if inputMethod=="file":
		print("URL filename?")
		f=open(sys.stdin.readline().rstrip(), "r")
		
	elif inputMethod=="console":
		print("Enter EOF character (^D) to stop entering data.")
		f=sys.stdin

	elif inputMethod=="dirlisting":
		print("Directory to list?")
		basedir=sys.stdin.readline().rstrip()

		if basedir==".":
			basedir=os.getcwd()

		dirList=os.listdir(basedir)
		
		for entry in dirList:
			d.urlList.append("file://"+basedir+"/"+entry)

		#d.urlList=os.listdir(sys.stdin.readline())
		d.writeFile(d.datasetName+".def")
		return

	contents=f.read()
	lines=contents.splitlines()

	for l in lines:
		d.urlList.append(l)
	d.writeFile(d.datasetName+".def")

	f.close()
	return

def doCreateArgs():
	m=""
	methodData=""
	name=""

	d=DatasetDefs.Def()

	# Parse through arguments:
	for i in range(2, len(sys.argv), 1):
		argChunks=sys.argv[i].split('=')
		
		if argChunks[0]=="--name":
			if len(argChunks)==1:
				print("Error: no dataset name specified.")
				printCreateHelp()
			else:
				name=argChunks[1]

		elif argChunks[0]=="--dirlisting":
			if len(argChunks)==1:
				print("Error: no directory path specified.")
				printCreateHelp()
			else:
				methodData=argChunks[1]
				m="dirlisting"

		elif argChunks[0]=="--console":
			m="console"

		elif argChunks[0]=="--file":
			if len(argChunks)==1:
				print("Error: no filename specified.")
				printCreateHelp()
			else:
				methodData=argChunks[1]
				m="file"

	if m=="":
		print("Error: No URL input method specified.")
		printCreateHelp()

	elif name=="":
		print("Error: no dataset name specified.")
		printCreateHelp()

	d.datasetName=name
	f=None

	if m=="dirlisting":
		if methodData==".":
			methodData=os.getcwd()

		dirListing=os.listdir(methodData)

		for entry in dirListing:
			d.urlList.append("file://"+methodData+"/"+entry)

		d.writeFile(name+".def")
		return
	elif m=="file":
		f=open(methodData, "r")
	elif m=="console":
		print("Enter EOF character (^D) to stop entering data.")
		f=sys.stdin

	contents=f.read()
	d.urlList=contents.splitlines()
	d.writeFile(name+".def")

	f.close()
	return

def doShow(datasetName):
	d=DatasetDefs.Def(datasetName+".def")
	
	for u in d.urlList:
		print u

	return

if len(sys.argv)==1:
	printUsage()

curAction=sys.argv[1];

if curAction=="fetch":
	if len(sys.argv)<3:
		print("Please specify a dataset to fetch.")
	else:
		doFetch(sys.argv[2])

elif curAction=="list":
	doList()

elif curAction=="create":
	if len(sys.argv)<3:
		doCreate()
	else:
		doCreateArgs()

elif curAction=="show":
	if len(sys.argv)<3:
		print("Please specify a dataset to get more information about.")
	else:
		doShow(sys.argv[2])
