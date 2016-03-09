# genericfetch.py -- A generic dataset fetch dependency.
# Accepts the following arguments:
#   datasetname - Name of the dataset to fetch
#   dest        - Destination path for the dataset.

import ariadneplugin
import os
import time

plugin_class = "genericfetch"

class genericfetch(ariadneplugin.Plugin):
    name="genericfetch"
    datasetname=""
    dest=""


    def run(self):
        self.start_t=time.time()
        print("ariadne.py dataset fetch %s %s" % (self.datasetname, self.dest))
        os.system("ariadne.py dataset fetch %s %s" % (self.datasetname, self.dest))
        self.stop_t=time.time()


    def validate(self):
        return 1


    def __init__(self, args={}, conffile="", conftoks=[]):
        if args == {}:
            return
        self.datasetname=args['datasetname']
        self.dest=args['dest']
