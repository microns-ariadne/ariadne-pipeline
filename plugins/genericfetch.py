# genericfetch.py -- A generic dataset fetch dependency.
# Accepts the following arguments:
#   datasetname - Name of the dataset to fetch
#   dest        - Destination path for the dataset.

import ariadneplugin
import os

plugin_class = "genericfetch"

class genericfetch(ariadneplugin.Plugin):
    name="genericfetch"
    datasetname=""
    dest=""


    def run(self):
        # Workaround for development:
        prefix=""
        try:
            dirlisting=os.listdir(".")
            dirlisting.index("ariadne.py")
            prefix="./"
        except ValueError:
            prefix=prefix # Effectively do nothing.

        print(prefix+"ariadne.py dataset fetch %s %s" % (self.datasetname, self.dest))
        os.system(prefix+"ariadne.py dataset fetch %s %s" % (self.datasetname, self.dest))


    def validate(self):
        return 1


    def __init__(self, args={}, conffile="", conftoks=[]):
        if args == {}:
            return

        self.datasetname=args['datasetname']
        self.dest=args['dest']
