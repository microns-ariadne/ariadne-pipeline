# Pipeline.py -- Class and function definitions to build, manage, execute, and write pipelines.

import os

# An individual stage in the pipeline.
class Stage:
	dependencies=[]
	arguments=[]
	commands=[]
	name=""

	# Returns the raw dependency values rather than just their function
	# notation. Ie: extract vs extract(FILENAME,DEST)
	def getRawDependencies(self):
		rawList=[]

		for d in dependencies:
			stripped=d.replace('(', ' ')
			rawList.append(stripped.split(' ')[0])

		return rawList

	# Accepts a command as well as a set of argument<>value pairs.
	# Returns the ID of the new process.
	def __execCmd(self, cmdStr, argv):
		cmdString=""
		procArgs=[]

		# Start by tokenizing the string:
		cmdStr=cmdStr.replace('\t', ' ')
		cmdToks=cmdStr.split(' ')

		for t in cmdToks:
			found=0
			for a in argv:
				if t==a[0]:
					procArgs.append(a[1])
					found=1

			if not found:
				procArgs.append(t)

		return os.spawnvp(os.P_NOWAIT, cmdToks[0], procArgs)
	
	# Accepts a set of argument<>value pairs.
	# Returns a list of PIDs.
	def execute(self, args):
		pidList=[]

		for c in self.commands:
			pidList.append(self.__execCmd(c, args))

		return pidList

	def writeFile(self, filename):
		f=open(filename, "w")
		f.write("name: "+self.name+"\n")
		f.write("type: stage\n")

		f.write("dependencies:\n")
		
		for d in self.dependencies:
			f.write(d+"\n")

		f.write("arguments:\n")
		
		for arg in self.arguments:
			f.write(arg+"\n")

		f.write("commands:\n")

		for c in self.commands:
			f.write(c+"\n")

		f.close()
	
	# Either does nothing or reads the contents of a stage definition file.
	def __init__(self, filename=""):
		if filename=="":
			return

		# Do some file loading stuff.
		f=open(filename, "r")
		contents=f.read()
		f.close()
		
		contents=contents.replace('\t', ' ')
		linesList=contents.splitlines()

		prevType=""
		prevList=[]

		for l in linesList:
			tokens=l.split(' ')
			
			if len(tokens)>0:
				if tokens[0]=="name:":
					self.name=tokens[1]

				elif tokens[0]=="type:":
					if tokens[1]!="stage":
						return

				elif (tokens[0]=="dependencies:" or tokens[0]=="commands:" or tokens[0]=="arguments:") and (tokens[0]!=prevType):
					if prevType=="commands:":
						self.commands=prevList
					elif prevType=="arguments:":
						self.arguments=prevList
					elif prevType=="dependencies:":
						self.dependencies=prevList
					prevType=tokens[0]
					prevList=[]
					
					# In case there are any other tokens on the same line:
					for i in range(1, len(tokens), 1):
						prevList.append(tokens[i])

				else:
					prevList.append(l)

		# Do one final check to see if everything has been flushed out:
		if prevType=="commands:":
			self.commands=prevList
		elif prevType=="arguments:":
			self.arguments=prevList
		elif prevType=="dependencies:":
			self.dependencies=prevList

# Represents a tree of dependencies.
# In reality it's implemented as a ragged array.
class Deptree:
	contents=[]

	def getLayer(self, layer):
		return self.contents[layer]

	# This gets all possible dependency names so that they may be loaded.
	def __rcsvGetDeps(self, stage):
		depList=[]

		for d in stage.dependencies:
			rawDeps=stage.getRawDependencies()
			
			depList.extend(rawDeps)

			for r in rawDeps:
				st=Stage(r+".stage")
				depList.extend(self.__rcsvGetDeps(st))

		return depList
	
	# Loads all dependent stage descriptions from disk and returns them.
	def loadStages(self, stage):
		stageList=[]

		nameList.append(stage.name)
		stageList.append(stage)

		rawList=[]
		rawList.extend(self.__rcsvGetDeps(stage))
		rllen=len(rawList)

		cleanList=[]

		# Filter the raw list for duplicates:
		for i in range(0, (rllen-1), 1):
			tmpClean=1;
			tmp=rawList.pop()

			for element in cleanList:
				if element==tmp:
					tmpClean=0
					break

			if tmpClean:
				cleanList.append(tmp)

		for name in cleanList:
			stageList.append(Stage(name+".stage"))

		return stageList

	def __init__(self, stage):
		return

# The pipeline itself.
class Pipeline:
	dTree=None
	
