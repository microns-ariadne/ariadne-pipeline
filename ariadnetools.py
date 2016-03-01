# This is a flat set of functions that are useful to the rest of the project

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
