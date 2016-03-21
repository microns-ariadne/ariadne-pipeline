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


def write_file(tokens, f):
    for t in tokens:
        f.write("%s:\n" % t[0])
        for entry in t[1:]:
            f.write("\t%s\n" % entry)


def parse_block(lines):
    """Recursively parses through a block."""

    toklist=[]
    curtok=""
    lineidx=1

    toklist.append(lines[0].strip(':').strip())

    curtok=lines[lineidx].strip()

    while curtok!="end":
        tmp=curtok.strip(':')

        # Determine if we have another definition:
        if len(curtok)!=len(tmp):
            appendlist, tmpidx=parse_block(lines[lineidx:])
            toklist.append(appendlist)
            lineidx+=tmpidx
        elif len(curtok)==0:
            pass
        else:
            toklist.append(curtok)

        lineidx+=1

        if lineidx>=len(lines):
            break

        curtok=lines[lineidx].strip()

    return toklist, lineidx
            

def parse_nested_stream(f):
    contents=f.read()
    offset=0
    top=[]

    lines=contents.splitlines()

    while offset<(len(lines)-1):
        if lines[offset]!="end" and lines[offset]!='':
            tmparr, tmp=parse_block(lines[offset:])
            top.append(tmparr)
            offset+=tmp
        else:
            offset+=1

    return top


def parse_pipeline(filename):
    """Parses a pipeline definition file.
       This is a separate function from parse_file for backwards compatibility
    """

    f=open(filename, "r")
    tokens=parse_nested_stream(f)
    f.close()

    return tokens


class StageInfo:
    """ Parses and contains information about a stage definition. """
    name=""
    plugin_name=""
    args=[]
    exectype="run"


    def __init__(self, stagedef):
        if not len(stagedef):
            return

        self.name=stagedef[0]

        # Search for execution type:
        for d in stagedef[1:]:
            toks=d.split()

            if len(toks)>0:
                cmd=toks[0].strip(':')

                if cmd=="runtype":
                    self.exectype=toks[1]
                elif cmd=="args":
                    self.args=toks[1:]
                elif cmd=="plugin":
                    self.plugin_name=toks[1]
        
