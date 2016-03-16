# A newer, shinier implementation of pipeline
# that supports the changes made to ariadne's execution model (it's luigi time!)

import os
import sys
import tools
import deftools
import plugin
import luigi
import plugingen
import time


class Pipeline:
    stagenames=[]
    trainstagenames=[]
    datasets=[]
    env=[]
    plugindir=""


    def __setenv(self):
        for e in self.env:
            toks=e.split('=')
            try:
                os.environ[toks[0]]+=toks[1]
            except:
                os.environ[toks[0]]=toks[1]


    def __gen_depends(self, f, plugin):
        for d in plugin.depends():
            depclass=plugin.search_plugins(d.dependency_name)
            dep=depclass()
            # Go recursion!
            self.__gen_depends(f, dep)
        plugingen.gen(plugin, f, plugin.name, self.plugindir)


    def __loadplugins(self):
        if self.plugindir!="":
            tools.init_plugins(self.plugindir)
        else:
           self.plugindir=tools.get_base_dir()+"/plugins"


    def run(self, arglist):
        start=time.time()
        self.__setenv()
        self.__loadplugins()
        for s in self.stagenames:
            fname=s+"_l.py"
            f=open(fname, "w")
            pclass=plugin.search_plugins(s)
            if pclass==None:
                print("ERROR: Plugin not found: "+s)
                raise Exception
            else:
                self.__gen_depends(f, pclass())
                
            f.close()
            runstr="python -m luigi --module %s_l %s_l --local-scheduler" % (s, s)
            for a in arglist:
                runstr+=" --%s %s" % (a[0], a[1])
            os.system(runstr)
        return time.time()-start


    def __init__(self, def_filename):
        toks=deftools.parse_file(def_filename)
        td=deftools.make_dict(toks)
        
        if not len(td['stages']):
            print("ERROR: There must be at least one 'stage:' listing in the pipeline.")
            raise Exception
        else:
            self.stagenames=td['stages']
        
        try:
            self.trainstagenames=td['training']
        except:
            print("Warning: no training stages defined.")
        
        try:
            self.datasets=td['datasets']
        except:
            self.datasets=self.datasets

        self.env=td['environment']

        if len(td['plugindir']):
            self.plugindir=td['plugindir'][0]
