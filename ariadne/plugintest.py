import ariadneplugin
import sys

plugin_class="MyPlugin"

class MyPlugin(ariadneplugin.Plugin):
    name="MyPlugin"
    
    def run(self, args):
        print("I'm running! Woo!")
        
sys.path.append(".")
c=ariadneplugin.load_plugin("plugintest")

cl=c()

cl.run(None)
print("C's name is: "+c.name)