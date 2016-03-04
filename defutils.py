# Defutils.py -- Contains parsing functions for definition files.

# Produces an organized list of tokens in the file.
def parse(filename):
    f=open(filename, "r")
    contents=f.read()
    f.close()

    # Tokenize the file:
    #contents=contents.replace('\t', '\n')
    lines=contents.splitlines()

    outList=[]
    for l in lines:
        if l[len(l)-1]==':':
            outList.append([l.rstrip(':')])
        elif l!="":
            outList[len(outList)-1].append(l)

    return outList

def search(tokList, key):
    for tok in tokList:
        if tok[0]==key:
            return tok
    return []

def write(tokList, filename):
    f=open(filename, "w")

    for tok in tokList:
        f.write(tok[0]+":\n")
        for i in range(1, len(tok), 1):
            f.write(tok[i]+"\n")

    f.close()

class InvalidTypeException(Exception):
    typestr=""
    def __init__(self, value="File cannot be read properly."):
        typestr=value

    def __str__(self):
        return "InvalidTypeException: "+typestr

class DefFormatException(Exception):
    typestr=""
    def __init__(self, value="Definition format error."):
        typestr=value

    def __str__(self):
        return "DefFormatException: "+typestr

