# mkdir.py -- Generic ariadne plugin to make a directory.

import ariadneplugin
import os

plugin_class="mkdir"


class mkdir(ariadneplugin.Plugin):
    name="mkdir"
    dirname=""


    def run(self):
        os.system("mkdir -p "+self.dirname)


    def validate(self):
        return os.path.isdir(self.dirname)


    def __init__(self, args={}, conffile="", conftoks=[]):
        if args=={} and conffile=="" and conftoks==[]:
            return

        self.dirname=args['dirname']
