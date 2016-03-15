#!/usr/bin/env python
# shell2pipe.py -- A quick 'n dirty utility to convert simple shell scripts
#                  to ariadne pipelines.

import os
import sys
import datetime


def printusage():
    print("Usage: shell2pipe <script.sh> <output_dir> <pipe_name>")


def getname(dir_name, plugin_name):
    return dir_name+"/"+plugin_name+".py"


def genwrapper(f, name, line):
    f.write("# generated by shell2pipe on %s\n" % str(datetime.date.today()))
    f.write("import os\nimport plugin\n\n")
    f.write("plugin_class='%s'\n\n\n" % name)
    f.write("class %s(plugin.AriadneOp):\n" % name)
    f.write("    name='%s'\n\n\n" % name)
    f.write("    def run(self, args):\n")
    f.write("        os.system('%s')\n" % line)


def writepdef(f, plist, elist, dname):
    f.write("stages:\n")
    for p in plist:
        f.write("\t%s\n" % p)

    f.write("environment:\n")
    for e in elist:
        f.write("\t%s\n" % e)

    f.write("plugindir:\n")
    f.write("\t%s\n" % dname)


def genplist(f, plist):
    for p in plist:
        f.write("AriadneOp %s\n" % p)


def convert(script_name, dir_name, pipedef_name):
    f=open(script_name, "r")
    contents=f.read()
    f.close()
    lines=contents.splitlines()

    next_plugin_name=""
    plugin_list=[]
    env_list=[]

    pdeff=open(pipedef_name+".pipeline", "w")

    for l in lines:
        if len(l)>0:
            ltoks=l.split()
            if l[0]=='#':
                next_plugin_name=l[1:].strip()
                plugin_list.append(next_plugin_name)
            elif ltoks[0]=="export":
                env_list.append(ltoks[1])
            else:
                f=open(getname(dir_name, next_plugin_name), "w")
                genwrapper(f, next_plugin_name, l)
                f.close()

    writepdef(pdeff, plugin_list, env_list, dir_name)
    pdeff.close()
    f=open(dir_name+"/plugins.list", "w")
    genplist(f, plugin_list)
    f.close()
    

def main(args):
    if len(args)<4:
        printusage()
        return

    convert(args[1], args[2], args[3])


if __name__=="__main__":
    main(sys.argv)
