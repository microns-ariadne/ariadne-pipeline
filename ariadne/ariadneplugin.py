# ariadneplugin.py -- Contains classes and functoins necessary to implement a plugin architecture for
# ariadne.
import os
import sys
import ariadnetools


PLUGIN_TYPE_ARCHIVE="ArchivePlugin"
PLUGIN_TYPE_GENERIC="Plugin"
PLUGIN_TYPE_DATASET="DatasetPlugin"
PLUGIN_TYPE_VALIDATION="ValidationPlugin"

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


def search_plugins(plugin_name):
    for p in plugin_list:
        o=p[0]()
        if o.name==plugin_name:
            return p[0]
    return None


def get_can_handle(ext):
    for p in plugin_list:
        if p[1]!=PLUGIN_TYPE_GENERIC:
            pl=p[0]()
            if pl.can_handle(ext):
                return p[0]
    return None


class DatasetPlugin:
    # Note: this class is defined at the bottom of the file because it makes
    # use of the ability to search for other plugins.
    name=None
    data_list=[]
    
    def can_handle(self, dataset_type):
        return 0
    

    def validate(self):
        return 0
    
    
    def fetch(self, destination):
        basedir=ariadnetools.get_base_dir()
        for d in self.data_list:
            os.system(basedir+"/scripts/ariadne-fetch.sh "+d+" "+destination)
            return 1


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
                return 1

    def get_file_list(self, destination):
        # This and get_file exist so that stages can get data for themselves.
        return os.listdir(destination)


    def get_file(self, destination, name, mode):
        return open(destination+"/"+name, mode)


    def __init__(self, def_filename="", def_tokens=[]):
        return


class ArgException(Exception):
    custom_message=""
    

    def __init__(self, msg=""):
        self.custom_message=msg


    def __str__(self):
        return "Invalid arguments.\n"+self.custom_message


class DependencyContainer:
    dependency_name=""
    arg_dict={}
    

    def __init__(self, depname, args):
        self.arg_dict=args
        self.dependency_name=depname


class Plugin:
    name=None
    argnames=[]
    debugging_args={}
    start_t=0
    stop_t=0

    
    def run(self):
        return

    
    def depends(self):
        # Should return a list of DependencyContainers.
        return []


    def validate(self):
        return 0

    
    def check_inputs(self):
        return


    def benchmark(self):
        return self.stop_t-self.start_t


    def success(self):
        return 1


    def print_benchmark(self):
        print("Benchmark completed in: "+str(self.benchmark())+" seconds.")

    
    def __init__(self, args={}, conffile="", conftoks=[]):
        self.debugging_args=args
        return


class ArchivePlugin:
    name=None
    
    
    def can_handle(self, extension):
        return 0
    
    
    def unpack(self, file_name, destination):
        return
    
    
    def __init__(self):
        return


class ValidationPlugin:
    # This plugin type should make it easier for other 
    # plugins to validate themselves and their output.
    # It is ultimately a very flexible plugin class, 
    # and it is expected that each validation plugin be
    # requested by name or very specific handler type.
    name=None
    
    
    def get_handler(self, extension):
        # Should return a method that can handle the extension requested.
        # That method's arguments and return value are implementation-dependent.
        return None
    
    
    def can_handle(self, extension):
        # Should return whether or not this plugin can handle the 
        # handler type specified.
        return 0
    

    def get_actions_handled(self):
        # Should return the list of extensions or handler types
        # that this plugin can handle.
        return []


    def __init(self):
        return