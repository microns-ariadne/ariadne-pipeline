# This file contains definitions and classes related to ariadne-dataset.
import ariadnetools
import defutils
import os

class Def:
    # Have some internal state handy:
    urlList=[]
    datasetName=""
    validationScript=""
    formatSpec=[]

    def validate(self):
        scriptToks=self.validationScript.replace('\t', ' ').split(' ')
        return os.spawnvp(os.P_WAIT, scriptToks[0], scriptToks)
    
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

        filetoks=defutils.parse(fileName)

        # Validate the file type:
        fileType=defutils.search(filetoks, "type")
        if len(fileType)>1:
            if fileType[1]!="dataset":
                raise defutils.InvalidTypeException()

        tmp=defutils.search(filetoks, "name")
        if len(tmp)>1:
            self.datasetName=tmp[1]

        tmp=defutils.search(filetoks, "urls")
        if len(tmp)>1:
            self.urlList=tmp[1:]

        tmp=defutils.search(filetoks, "formatspec")
        if len(tmp)>1:
            self.formatSpec=tmp[1:]

        tmp=defutils.search(filetoks, "validationscript")
        if len(tmp)>1:
            self.validationScript=tmp[1]
