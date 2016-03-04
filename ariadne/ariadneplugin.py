# ariadneplugin.py -- Contains classes and functoins necessary to implement a plugin architecture for
# ariadne.
import os
import sys
import ariadnetools

class Plugin:
    name=None

    
    def run(self, args):
        return

    
    def validate(self, args):
        return

    
    def check_inputs(self):
        return


    def benchmark(self):
        return

    
    def __init__(self, conffile=""):
        return


class ArchivePlugin:
    name=None
    
    
    def can_handle(self, extension):
        return 0
    
    
    def unpack(self, file_name, destination):
        return
    
    
    def __init__(self):
        return


PLUGIN_TYPE_ARCHIVE="ArchivePlugin"
PLUGIN_TYPE_GENERIC="Plugin"
PLUGIN_TYPE_DATASET="DatasetPlugin"

# Entry format: [0]=plugin object, [1]=plugin type.
plugin_list=[]


def load_plugin(module_name):
    mod=__import__(module_name)

    if hasattr(mod, 'plugin_class'):
        return getattr(mod, mod.plugin_class)
    else:
        print("ERROR: Module "+module_name+" did not define a plugin name.")
        exit(1)


def load_plugins(list_file, base_dir):
    f=open(list_file, 'r')
    contents=f.read()
    plugin_names=contents.splitlines()
    
    try:
        sys.path.index(base_dir)
    except:
        sys.path.append(base_dir)
    
    # Plugin entries are formatted as: type plugin\n
    for name in plugin_names:
        name_tokens=name.split()
        plugin_list.append([load_plugin(name_tokens[1]), name_tokens[0]])


def get_plugins(plugin_type):
    ret_list=[]
    
    for p in plugin_list:
        if p[1]==plugin_type:
            ret_list.append(p)
    
    return ret_list


class DatasetPlugin:
    # Note: this class is defined at the bottom of the file because it makes
    # use of the ability to search for other plugins.
    name=None
    data_list=[]
    
    def can_handle(dataset_type):
        return 0
    
    def validate(self):
        return
    
    
    def fetch(self, destination):
        basedir=ariadnetools.get_base_dir()
        for d in self.data_list:
            os.system(basedir+"scripts/ariadne-fetch.sh "+d+" "+destination)


    def unpack(self, destination):
        if destination == "":
            destination = "."
        contents = os.listdir(destination)
        archive_plugins = get_plugins(PLUGIN_TYPE_ARCHIVE)
        for c in contents:
            ext = ariadnetools.get_extension(c)
            
            for a in archive_plugins:
                p=a[0]()
                if p.can_handle(ext):
                    p.unpack(destination+"/"+c, destination)


    def __init__(self, def_filename=""):
        return