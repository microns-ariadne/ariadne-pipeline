# pipeline.py -- Contains classes and functions related to running and managing the pipeline.
import deftools
import ariadnetools
import ariadneplugin
import os
import sys

class Pipeline:
    topmodule=None
    topmodule_name=""
    topmodule_args={}
    name=""

    def __runplugin(self, plugin, args):
        for d in plugin.depends():
            # Try to find the plugin:
            depclass=ariadneplugin.search_plugins(d.dependency_name)
            if depclass!=None:
                dep=depclass()
                self.__runplugin(dep, d.arg_dict)
            else:
                print("ERROR: Unresolved dependency. Name: "+d.dependency_name)
        plugin.run(args)

    def run(self):
        tm=self.topmodule()
        
        self.__runplugin(tm, self.topmodule_args)
            
        
    def __init__(self, deffilename="", args={}):
        if deffilename=="":
            return
        
        self.topmodule_args=args
        
        tokens=deftools.parse_file(deffilename)
        
        self.topmodule_name=deftools.search(tokens, "topmodule")[0]
        self.name=deftools.search(tokens, "name")[0]
        
        self.topmodule=ariadneplugin.search_plugins(self.topmodule_name)