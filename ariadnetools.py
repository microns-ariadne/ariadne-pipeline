# This is a flat set of functions that are useful to the rest of the project
import os

# Gets a file extension from a URL or filename:
def getExtension(name):
	tmp=name.split('.')

	retStr=""

	for i in range(1, len(tmp), 1):
		retStr=retStr+"."+tmp[i]

	return retStr

def getUrlFilename(url):
	tmp=url.split('/')
	
	if len(tmp)>0:
		return tmp[len(tmp)-1]
	else:
		return ""

def getUrlExtension(url):
	tmp=getUrlFilename(url)
	
	return getExtension(tmp)

def getDefAttrib(filename, attribname):
	attribname=attribname+":"
	f=open(filename, "r")

        contents=f.read()    
        contents=contents.replace("\t", "\n")
        contents=contents.replace(" ", "\n") 
        lines=contents.splitlines()

        for i in range(0, len(lines)-1, 1):
                if lines[i]==attribname:
                        if (i+1)<len(lines):
                                return lines[i+1]

	f.close()
        return "undefined"

def getDefType(filename):
	return getDefAttrib(filename, "type")

def getDefName(filename):
	return getDefAttrib(filename, "name")

def fileExists(filename, extensions=[]):
	if extensions==[]:
		return os.path.isfile(filename)

	curStatus=0

	for e in extensions:
		curStatus=curStatus or fileExists(filename+e)

	return curStatus

# Removes any blank strings from the specified list.
def trimBlankStrings(arr):
	while 1:
		try:
			arr.remove('')
		except ValueError:
			break

# Pairs off arguments and values.
def argPair(argv, startArg=0):
	argList=[]
	
	for a in argv[startArg:]
		toks=a.split('=')
		if len(toks)==1:
			toks.append("")
		argList.append(toks)
	return argList

# Strips all strings in a list.
def stripList(lst, stripStr=""):
	retList=[]
	
	for s in lst:
		if stripStr=="":
			retList.append(s.strip())
		else:
			retList.append(s.strip(stripStr))

	return retList
