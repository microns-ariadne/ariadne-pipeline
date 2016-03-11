# A new pipeline as I clean out the old one.
# pipeline.py -- Contains classes and functions related to running and managing the pipeline.
import deftools
import ariadnetools
import ariadneplugin
import os
import sys
import time
from multiprocessing import Process, Value
import workerinterface


class Pipeline:
    topplugin=None
    topplugin_name=""
    topplugin_args={}
    name=""
    env_vars=[]
    env_vars_append=[]
    pipe_plugin_dir=""
    last_plugin_args={}
    dep_list=[]
    exec_plugin_name=""


    def __build_dep_list(self, plugin, dlevel, args):
        # This should allow for simple parallel processing to take place.
        self.dep_list.append([dlevel, plugin, args])
        p=plugin(args)
        for d in p.depends():
            depclass=ariadneplugin.search_plugins(d.dependency_name)
            if depclass != None:
                self.__build_dep_list(depclass, dlevel+1, d.arg_dict)
            else:
                print("ERROR: Unresolved dependency. Name: "+d.dependency_name)
                exit(2)


    def __get_max_dlevel(self):
        maxd=0
        for d in self.dep_list:
            if d[0] > maxd:
                maxd=d[0]
        return maxd


    def __get_of_dlevel(self, dlevel):
        dlist=[]
        
        for d in self.dep_list:
            if d[0] == dlevel:
                dlist.append(d)
        
        return dlist


    def __runplugin(self, plugin, args, eplugin, validation_mode, benchmark_mode):
        print("Building dependency list...")
        self.__build_dep_list(plugin, 0, args)
        print("Finding highest level dependency...")
        highest=self.__get_max_dlevel()
        for i in range(highest, -1, -1):
            print("Executing level: "+str(i))
            deplist=self.__get_of_dlevel(i)
            # Now try to build a proper execution list for the plugin:
            elist=[]
            for d in deplist:
                tmp=ariadneplugin.ExecutionWrapper()
                tmp.plugin_name=d[1]
                tmp.plugin_args=d[2]
                elist.append(tmp)
            # Now run the list:
            plugin.run(elist, validation_mode, benchmark_mode)
        return self.dep_list[0][1](self.dep_list[0][2])


    def __set_environment(self):
        for e in self.env_vars:
            print("Installing environment variable: " + e)
            toks = e.split('=')
            os.environ[toks[0]] = toks[1]
        for e in self.env_vars_append:
            toks = e.split('=')
            os.environ[toks[0]] += toks[1]
        

    def run(self, pipe_args, validation_mode=0, benchmark_mode=0):
        """Runs a pipeline"""
        # Start by determining which execution plugin was specified:
        eplugin_class=ariadneplugin.search_plugin(self.exec_plugin_name)
        if eplugin_class==None:
            print("ERROR: Could not find execution plugin: "+self.exec_plugin_name)
        eplugin=eplugin_class
        start=time.time()
        tpl=self.__runplugin(self.topplugin, pipe_ars, eplugin, validation_mode, benchmark_mode)
        total=time.time()-start

        if benchmark_mode:
            print("Total time taken to execute the pipeline: "+str(total))

        return tpl

            
    def validate(self, arglist):
        self.run(argdict, 1, 0)


    def benchmark(self, argdict):
        self.run(argdict, 0, 1)
    

    def check_dependencies(self):
        """Checks dependencies. Will eventually be moved to an execution plugin."""
        retv=self.__rcsv_get_dep_list(self.topplugin_name)
        if retv==0:
            print("ERROR: Not all dependencies satisfied.")
        else:
            print("All dependencies present.")


    def __init__(self, deffilename="", deftoks=[]):
        if deffilename=="":
            return        

        tokens=[]
        if deftoks == []:
            tokens = deftools.parse_file(deffilename)
        else:
            tokens=deftoks
        
        self.env_vars=deftools.search(tokens, "environment")
        self.env_vars_append=deftools.search(tokens, "environment_append")
        # Allow the user to specify plugins specifically for some task:
        tmp=deftools.search(tokens, "localplugins")
        if len(tmp)>0:
            ariadnetools.init_plugins(tmp[0])

        tmp=deftools.search(tokens, "execplugin")
        if len(tmp)>0:
            # Allow users to potentially specify an alternative execution method.
            self.exec_plugin_name=tmp[0]
        else:
            # Default to the serial executor.
            self.exec_plugin_name="serial_executor"

        self.topplugin_name=deftools.search(tokens, "topplugin")[0]
        self.exec_plugin_name=deftools.search(tokens, "execplugin")[0]
        self.name=deftools.search(tokens, "name")[0]
        self.topplugin=ariadneplugin.search_plugins(self.topplugin_name)
