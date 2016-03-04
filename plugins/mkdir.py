# mkdir.py -- Generic ariadne plugin to make a directory.

import ariadneplugin
import os

plugin_class="mkdir"


class mkdir(ariadneplugin.Plugin):
    name="mkdir"


    def run(self, args):
        dirname=args['dirname']
        
        os.system("mkdir -p "+dirname)