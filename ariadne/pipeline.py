# pipeline.py -- Contains classes and functions related to running and managing the pipeline.
import deftools
import ariadnetools
import ariadneplugin
import os
import sys
import time
from multiprocessing import Process, Value

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


    def __build_dep_list(self, plugin, dlevel):
        # This should allow for simple parallel processing to take place.
        self.dep_list.append([dlevel, plugin])
        for d in plugin.depends():
            depclass=ariadneplugin.search_plugins(d.dependency_name)
            if depclass != None:
                dep=depclass(d.arg_dict)
                self.__build_dep_list(dep, dlevel+1)
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


    def __plugin_execution_wrapper(self, plugin):
        p=Process(target=plugin.run, args=())
        p.start()
        return p


    def __runplugin(self, plugin, validation_mode, step_by_step, benchmark_mode):
        print("Building dependency list...")
        self.__build_dep_list(plugin, 0)
        print("Finding highest level dependency...")
        highest=self.__get_max_dlevel()
        for i in range(highest, -1, -1):
            print("Executing level: "+str(i))
            elist=self.__get_of_dlevel(i)
            tpool=[]
            # Start with fork:
            for d in elist:
                if d[1].parallel:
                    tpool.append(self.__plugin_execution_wrapper(d[1]))
                else:
                    d[1].run()
            # Now join:
            for t in tpool:
                t.join()
            # Serial validation and benchmarking:
            for d in elist:
                if benchmark_mode:
                    d[1].print_benchmark()
                if validation_mode:
                    valresults=d[1].validate()
                    if valresults:
                        print("PASS:" + d[1].name)
                    else:
                        print("FAIL:" + d[1].name)
                if step_by_step:
                    print("Summary for stage: "+plugin.name)
                    print("\tArguments: "+str(plugin.debugging_args))
                    print("Press <Enter> to continue.")
                    sys.stdin.read(1)
                
                if not d[1].success():
                    print("ERROR: Could not successfully execute plugin: "+d[1].name)
                    exit(2)
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
        self.__set_environment()
        tpl = self.topplugin(pipe_args)
        start=time.time()
        self.__runplugin(tpl, validation_mode, step_by_step, benchmark_mode)
        total=time.time()-start
        if benchmark_mode:
            print("Total time taken to execute the pipeline: "+str(total))
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
