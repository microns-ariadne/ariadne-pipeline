# mkfiles.py - Creates two files and specifies dependencies.
# This is an example of a plugin with fixed functionality and
# a dependency tree that can be resolved by ariadne.

from ariadne import plugin
import os

plugin_class="mkfiles"


class mkfiles(plugin.AriadneOp):
    name="mkfiles"

    
    def run(self, arg_dict):
        filenames=arg_dict['filenames']
        contents=arg_dict['contents']

        for i in range(0, len(filenames)):
            f=file(filenames[i])
            f.write(contents[i])
            f.close()


    def depends(self):
        deplist=[]
        deplist.append(plugin.DependencyContainer("mkdirs", {'dirs': ['a', 'b']}))
        return deplist
