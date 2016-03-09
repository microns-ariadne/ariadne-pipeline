# pipeline.py -- Contains classes and functions related to running and managing the pipeline.
import deftools
import ariadnetools
import ariadneplugin
import os
import sys

class Pipeline:
    topplugin=None
    topplugin_name=""
    topplugin_args={}
    name=""
    env_vars=[]
    env_vars_append=[]
    pipe_plugin_dir=""
    #datasets=[]

    def __runplugin(self, plugin):
        for d in plugin.depends():
            print("Handling dependency: "+d.dependency_name)
            
            # Try to find the plugin:
            depclass = ariadneplugin.search_plugins(d.dependency_name)
            if depclass != None:
                dep = depclass(d.arg_dict)
                self.__runplugin(dep)
            else:
                print("ERROR: Unresolved dependency. Name: "+d.dependency_name)
        plugin.run()
        
        if plugin.success() == 0:
            print("ERROR: Could not successfully execute plugin: "+plugin.name)
            exit(2)


    def __set_environment(self):
        for e in self.env_vars:
            print("Installing environment variable: " + e)
            toks = e.split('=')
            os.environ[toks[0]] = toks[1]
        for e in self.env_vars_append:
            toks = e.split('=')
            os.environ[toks[0]] += toks[1]


    def __check_top_stage(self, curplugin):
        return curplugin.validate()


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
        

    def run(self, pipe_args):
        # TODO: Implement dataset fetching logic here.
        self.__set_environment()
        tpl = self.topplugin(pipe_args)
        self.__runplugin(tpl)
        return tpl

            
    def validate(self, arglist):
        passnum=0
        failnum=0
        for a in arglist:
            curplugin=self.run(a)
            if self.__check_top_stage(curplugin):
                print("PASS: "+a['test_name'])
                passnum += 1
            else:
                print("FAIL: "+a['test_name'])
                failnum += 1
        total=passnum+failnum
        print("Passed %d of %d tests. (%f pct)" % (passnum, total, passnum/total*100))


    def benchmark(self, argdict):
        tpl=self.topplugin(argdict)
        # It's up to the individual plugin to report stats like accuracy, etc.
        time_taken=tpl.benchmark()
        print("Benchmark completed in "+str(time_taken)+" seconds.")
        print("Benchmark arguments: "+str(argdict))
    

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
        #self.datasets=deftools.search(tokens, "datasets")
        self.topplugin=ariadneplugin.search_plugins(self.topplugin_name)
