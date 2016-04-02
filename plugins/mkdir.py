# mkdir.py -- Generic ariadne plugin to make a directory.

from ariadne import plugin
import os
import time

plugin_class="mkdir"


class mkdir(plugin.AriadneOp):
    name="mkdir"


    def get_arg_names(self):
        return ['dirname']


    def run(self, args):
        os.system("mkdir %s" % args['dirname'])
