import ariadneplugin
import os

plugin_class="testpipe1"


class testpipe1(ariadneplugin.Plugin):
    name="testpipe1"

    
    def depends(self):
<<<<<<< HEAD
        return [ariadneplugin.DependencyContainer("mkdir", {"dirname": "yarr"})]


    def __init__(self, args={}):
=======
        return [ariadneplugin.DependencyContainer("mkdir", {"dirname": "fancydir"})]


    def __init__(self):
>>>>>>> 7b623fc76fe125104b7e6e4c66bfe9d91d435b40
        return


    def run(self, args):
        filename=args['filename']
        filecontents=args['filecontents']
        
        f=open(filename, "w")
        f.write(filecontents)
        f.close()
