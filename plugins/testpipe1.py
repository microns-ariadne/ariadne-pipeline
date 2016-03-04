import ariadneplugin
import os

plugin_class="testpipe1"


class testpipe1(ariadneplugin.Plugin):
    name="testpipe1"

    
    def depends(self):
        return [ariadneplugin.DependencyContainer("mkdir", {"dirname": "fancydir"})]


    def __init__(self):
        return


    def run(self, args):
        filename=args['filename']
        filecontents=args['filecontents']
        
        f=open(filename, "w")
        f.write(filecontents)
        f.close()
