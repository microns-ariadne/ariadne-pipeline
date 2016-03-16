# mkdir.py -- Generic ariadne plugin to make a directory.

import ariadneplugin
import os
import time

plugin_class="mkdir"


class mkdir(ariadneplugin.Plugin):
    name="mkdir"
    dirname=""
    start=0
    stop=0


    def run(self):
        print("Makin' a dir: "+self.dirname)
        self.start=time.time()
        os.system("mkdir -p "+self.dirname)
        self.stop=time.time()


    def validate(self):
        return os.path.isdir(self.dirname)


    def benchmark(self):
        return self.stop-self.start


    def __init__(self, args={}, conffile="", conftoks=[]):
        if args=={} and conffile=="" and conftoks==[]:
            return

        self.dirname=args['dirname']
