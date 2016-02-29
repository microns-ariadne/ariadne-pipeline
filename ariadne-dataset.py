#!/usr/bin/env python

# ariadne-dataset -- Ariadne module to fetch, manage, and unpack datasets.

import os
import sys
import DatasetDefs

import ariadnetools

def printUsage():
	print("Usage: ariadne-dataset <command> [args]")
	print("")
	print("Where command is one of the following:")
	print("fetch  \t Fetch a dataset specified by name.")
	print("list   \t List all dataset files in the current directory.")
	print("create \t Creates a dataset definition file.")
	print("show   \t Print information about a dataset.")
	exit(1);

def doFetch(dsname):
	d=DatasetDefs.Def(dsname+".def")

	pids=[]
	
	# Fire off download jobs:
	for u in d.urlList:
		print("u:"+u)
		print("Extension: "+ariadnetools.getExtension(u))
		pids.append(os.spawnlp(os.P_NOWAIT, "ariadne-download.sh", "ariadne-download.sh", u))

	print("Fetching datasets...")

	for p in pids:
		status=os.waitpid(p, 0)
		rcode=status[1]&0xFF00
		
		print rcode
		if rcode!=0:
			print("Couldn't download a file.")

	return

def doList():
	return

def doCreate():
	return

def doShow():
	return

if len(sys.argv)==1:
	printUsage()

curAction=sys.argv[1];

if curAction=="fetch":
	if len(sys.argv)<3:
		print("Please specify a dataset to fetch")
	else:
		doFetch(sys.argv[2])

elif curAction=="list":
	doList()

elif curAction=="create":
	doCreate()

elif curAction=="show":
	doShow()
