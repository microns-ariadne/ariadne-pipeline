# mkdirs.py - A plugin that creates all directories in its argument list.
# This plugin is designed to be general-purpose. As such, it specifies no dependencies
# and accepts arguments that alter how it is to be executed. 

from ariadne import plugin
import os

plugin_class="mkdirs"


class mkdirs(plugin.AriadneOp): # A generic plugin to do directory creation tasks, etc.
    name="mkdirs"

    def run(self, arg_dict):
        dirs=arg_dict['dirs']
        for d in dirs:
            os.system('mkdir '+d)

