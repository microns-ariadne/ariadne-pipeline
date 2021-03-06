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
    stagedefs=[]
    trainstagenames=[]
    datasets=[]
    env=[]
    plugindir=""


    def __setenv(self):
        """Appends and installs all environment variables."""
        for e in self.env:
            toks=e.split('=')
            try:
                os.environ[toks[0]]+=toks[1]
            except:
                os.environ[toks[0]]=toks[1]


    def __gen_depends(self, f, pl, exectype, args):
        """Generates all files necessary to correctly execute the given plugin."""
        # Dependencies are handled by plugingen.
        plugingen.gen(pl, f, pl.name, self.plugindir, exectype, args)


    def __gen_test_depends(self, f, pl, exectype, args):
        """Generates all files necessary to correctly test and execute the given plugin."""
        plugingen.gentest(pl, f, pl.name, self.plugindir, exectype, args)


    def __loadplugins(self):
        """Attempts to load all plugins specified in the pipeline definition file."""
        print("Loading plugins from %s" % self.plugindir)
        if self.plugindir!="":
            tools.init_plugins(self.plugindir)
        else:
           self.plugindir=tools.get_base_dir()+"/plugins"


    def run(self, arglist):
        """Runs the pipeline."""
        start=time.time()
        # Start by getting information about each stage:
        self.__setenv()
        self.__loadplugins()

        for s in self.stagedefs:
            stageinfo=deftools.StageInfo(s)
            modname=stageinfo.plugin_name+"_"+stageinfo.exectype
            fname=modname+"_l.py"
            f=open(fname, "w")
            plugingen.genheader(f)
            pclass=plugin.search_plugins(stageinfo.plugin_name)
            if pclass==None:
                print("ERROR: Plugin not found: %s" % stageinfo.plugin_name)
                raise Exception
            else:
                self.__gen_depends(f, pclass(), stageinfo.exectype, stageinfo.args)

            f.close()
            runstr="python -m luigi --module %s_l %s_l --local-scheduler" % (modname, stageinfo.plugin_name)
            os.system(runstr)
            
        return time.time()-start


    def test(self, arglist):
        """Runs and then tests each pipeline module."""
        start=time.time()

        self.__setenv()
        self.__loadplugins()

        for s in self.stagedefs:
            stageinfo=deftools.StageInfo(s)
            modname=stageinfo.plugin_name+"_"+stageinfo.exectype+"_test"
            fname=modname+"_l.py"
            f=open(fname, "w")
            plugingen.genheader(f)
            pclass=plugin.search_plugins(stageinfo.plugin_name)

            if pclass==None:
                print("ERROR: Plugin not found: %s" % stageinfo.plugin_name)
                raise Exception
            else:
                self.__gen_depends(f, pclass(), stageinfo.exectype, stageinfo.args)

        return time.time()-start


    def __init__(self, def_filename):
        """Parses a pipeline definition file and sets up values for future pipeline execution."""
        toks=deftools.parse_pipeline(def_filename)
        td=deftools.make_dict(toks)
        
        if not len(td['stages']):
            print("ERROR: There must be at least one 'stages:' block in the pipeline.")
            raise Exception
        else:
            self.stagedefs=td['stages']
        
        try:
            self.datasets=td['datasets']
        except:
            self.datasets=self.datasets

        self.env=td['environment']

        try:
            print("Plugindir: "+str(td['plugindir']))
            if len(td['plugindir']):
                self.plugindir=td['plugindir'][0]
        except:
            print("No defined plugin directory.")
            pass
