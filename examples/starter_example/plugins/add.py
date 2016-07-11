# add.py - Top level module for the addition demo pipeline
# This plugin is, like mkfiles, fixed-function. It acts as a top level module
# and thus 

from ariadne import plugin
import os

plugin_class="add"


class add(plugin.AriadneOp):
    name="add"

    def run(self, arg_dict):
        f=file('a/a.txt')
        a=f.read()
        f.close()
        f=file('b/b.txt')
        b=f.read()
        f.close()

        a=int(a)
        b=int(b)
        c=a+b
        f=file('c/c.txt')
        f.write(str(c))
        f.close()

    def depends(self):
        deplist=[]
        deplist.append(plugin.DependencyContainer("mkfiles", {'filenames': ['a/a.txt', 'b/b.txt'], 'contents': ['1', '2']}))
        deplist.append(plugin.DependencyContainer("mkdirs", {'dirs': ['c']}))
        return deplist

    
    
