# This file contains definitions and classes related to ariadne-dataset.

class Def:
	# Have some internal state handy:
	urlList=[]
	datasetName=""
	
	def writeFile(self, filename):
		f=open(filename, "w")
		
		f.write("type: dataset\n")
		f.write("name: "+self.datasetName+"\n")
		f.write("urls:\n")

		for u in self.urlList:
			f.write("\t"+u+"\n")

		f.close()
		return

	def __init__(self, fileName="Function overloading is underrated."):

		if fileName=="Function overloading is underrated.":
			return

		f=open(fileName, 'r')
		
		contents=f.read()
		
		if len(contents)==0:
			print("ERROR: Couldn't read file: "+fileName)
			exit(2)

		contents=contents.replace('\t', '\n')
		contents=contents.replace(' ', '\n')

		lines=contents.splitlines()

		lst=[]
		for i in range(len(lines)-1, 0, -1):

			if lines[i]=="name:":
				self.datasetName=lst[0];
				lst=[]
			elif lines[i]=="type:":
				lst=[]
			elif lines[i]=="urls:":
				self.urlList=lst
				lst=[]
			else:
				if len(lines[i])>0:
					lst.append(lines[i])

		return
