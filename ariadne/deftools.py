# deftools.py -- contains functions related to reading and writing dataset 
#                and pipeline definition files.


def parse_stream(f):
    contents = f.read()
    lines = contents.splitlines()
    tokens = []

    for l in lines:
        stripped = l.strip()
        if len(stripped)!=0:
            if stripped[len(stripped)-1] == ':':
                tokens.append([stripped[:len(stripped)-1]])
            else:
                tokens[len(tokens)-1].append(stripped)
    return tokens

def parse_file(filename):
    f = open(filename, "r")
    tokens=parse_stream(f)
    f.close()
    
    return tokens

def search(tokens, section):
    for t in tokens:
        if t[0] == section:
            return t[1:]
    return []


def make_dict(tokens):
    tokdict={}
    
    for t in tokens:
        tokdict[t[0]]=t[1:]
    
    return tokdict