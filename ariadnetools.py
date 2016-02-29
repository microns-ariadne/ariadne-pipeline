# This is a flat set of functions that are useful to the rest of the project

# Gets a file extension from a URL or filename:
def getExtension(name):
	tmp=name.split('.')

	retStr=""

	for i in range(1, len(tmp), 1):
		retStr=retStr+"."+tmp[i]

	return retStr

def getUrlFilename(url):

def getUrlExtension(url):

