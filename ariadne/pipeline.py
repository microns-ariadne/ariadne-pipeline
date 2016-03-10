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


    def __build_dep_list(self, plugin, dlevel, args):
        # This should allow for simple parallel processing to take place.
        self.dep_list.append([dlevel, plugin, args])
        p=plugin(args)
        for d in p():
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


    def __plugin_execution_wrapper(self, plugin, args):
        workerinterface.run_local(plugin.name, args)


    def __plugin_join(self):
        workerinterface.wait_local()


    def __runplugin(self, plugin, args, validation_mode, step_by_step, benchmark_mode):
        if validation_mode:
            workerinterface.validate_local()
        if benchmark_mode:
            workerinterface.benchmark_local()

        print("Building dependency list...")
        self.__build_dep_list(plugin, 0, args)
        print("Finding highest level dependency...")
        highest=self.__get_max_dlevel()
        for i in range(highest, -1, -1):
            print("Executing level: "+str(i))
            elist=self.__get_of_dlevel(i)
            # Start with fork:
            for d in elist:
                self.__plugin_execution_wrapper(d[1], d[2])
            # Now join:
            self.__plugin_join()
        return self.dep_list[0][1]


    def __set_environment(self):
        for e in self.env_vars:
            print("Installing environment variable: " + e)
            toks = e.split('=')
            os.environ[toks[0]] = toks[1]
        for e in self.env_vars_append:
            toks = e.split('=')
            os.environ[toks[0]] += toks[1]


    def __rcsv_get_dep_list(self, pluginname):
        # TODO: write this efficiently. 
        pclass=ariadneplugin.search_plugins(pluginname)
        if pclass==None:
            return 0
        
        retv=1
        
        plugin=pclass()
        for d in plugin.depends():
            retv=retv and self.__rcsv_get_dep_list(d.dependency_name)
            
        return retv
        

    def run(self, pipe_args, validation_mode=0, step_by_step=0, benchmark_mode=0):
        workerinterface.init()
        workerinterface.connect_local()
        self.__set_environment()
        start=time.time()
        self.__runplugin(self.topplugin, pipe_args, validation_mode, step_by_step, benchmark_mode)
        total=time.time()-start
        if benchmark_mode:
            print("Total time taken to execute the pipeline: "+str(total))
        workerinterface.disconnect_local()
        return tpl

            
    def validate(self, arglist, step_by_step=0):
        passnum=0
        failnum=0
        for a in arglist:
            curplugin=self.run(a, 1, step_by_step, 0)
            if curplugin.validate():
                print("PASS: "+a['test_name'])
                passnum += 1
            else:
                print("FAIL: "+a['test_name'])
                failnum += 1
        total=passnum+failnum
        print("Passed %d of %d tests. (%f pct)" % (passnum, total, passnum/total*100))


    def benchmark(self, argdict):
        self.run(argdict, 0, 0, 1)
    

    def check_dependencies(self):
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

        self.topplugin_name=deftools.search(tokens, "topplugin")[0]
        self.name=deftools.search(tokens, "name")[0]
        self.topplugin=ariadneplugin.search_plugins(self.topplugin_name)
