# ariadneplugin.py -- Contains classes and functoins necessary to implement a plugin architecture for
# ariadne.
import os
import sys
import tools
import nose


PLUGIN_TYPE_ARCHIVE="ArchivePlugin"
PLUGIN_TYPE_GENERIC="Plugin"
PLUGIN_TYPE_DATASET="DatasetPlugin"
PLUGIN_TYPE_VALIDATION="ValidationPlugin"
PLUGIN_TYPE_EXECUTOR="ExecutorPlugin"

# Entry format: [0]=plugin object, [1]=plugin type.
plugin_list=[]


def load_plugin(module_name):
    """Loads a plugin and appends it to plugin_list."""
    mod=__import__(module_name)

    if hasattr(mod, 'plugin_class'):
        return getattr(mod, mod.plugin_class)
    else:
        print("ERROR: Module "+module_name+" did not define a plugin name.")
        exit(1)


def load_plugins(list_file, base_dir):
    """Loads all plugins given a base directory and a plugin list file."""
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
    """Returns a list of plugins that are of the specified type."""
    ret_list=[]
    
    for p in plugin_list:
        if p[1]==plugin_type:
            ret_list.append(p)
    
    return ret_list


def search_plugins(plugin_name):
    """Returns the first plugin with the specified name or None if not found."""
    for p in plugin_list:
        o=p[0]()
        if o.name==plugin_name:
            return p[0]
    return None


def get_can_handle(ext):
    """Returns the first plugin that can handle the specified extension."""
    for p in plugin_list:
        if p[1]!=PLUGIN_TYPE_GENERIC:
            pl=p[0]()
            if pl.can_handle(ext):
                return p[0]
    return None


config_dict={}


def set_config(conf_dict):
    """Sets the global configuration dictionary to the specified value."""
    global config_dict
    config_dict=conf_dict


def get_temp_filename(filename):
    """Returns the name of a valid temporary file."""
    global config_dict
    tmpdir=config_dict['tmpdir'][0]
    return tmpdir+"/"+filename


def get_dataset_real_list(dataset_filename):
    """Returns a list of files from a downloaded dataset"""
    global config_dict
    tmpdir=config_dict['tmpdir'][0]
    real_list=[]
    ds_toks=deftools.parse(dataset_filename)
    
    data_list=deftools.search(ds_toks, "urls")
    for d in data_list:
        real_list.append(tools.get_url_filename(d))


class ArgException(Exception):
    """Exception to specify cases where there are invalid/insufficient arguments
       to run the specified plugin.
    """
    custom_message=""
    

    def __init__(self, msg=""):
        self.custom_message=msg


    def __str__(self):
        return "Invalid arguments.\n"+self.custom_message


class DependencyContainer:
    """A simple container class for dependency-related information."""
    dependency_name=""
    arg_dict={}
    

    def __init__(self, depname, args):
        self.arg_dict=args
        self.dependency_name=depname


class Plugin:
    """A generic plugin. Should be replaced with AriadneOp."""
    name=None
    parallel=1
    argnames=[]
    debugging_args={}
    start_t=0
    stop_t=0

    
    def run(self):
        return

    
    def depends(self):
        # Should return a list of DependencyContainers.
        return []


    def benchmark(self):
        return

    def test(self):
        return nose.run()


    def print_benchmark(self):
        print("Benchmark completed in: "+str(self.benchmark())+" seconds.")

    
    def __init__(self, args={}, conffile="", conftoks=[]):
        self.debugging_args=args
        return


class DatasetPlugin:
    """A special class of plugin intended to fetch and manage datasets."""
    name=None
    data_list=[]
    
    def can_handle(self, dataset_type):
        """Should return 1 if this plugin can handle the specified dataset type."""
        return 0
    

    def validate(self):
        """Validates the integrity of a dataset and returns a boolean
           representing whether the dataset passed all checks.
        """
        return 0
    
    
    def fetch(self, destination):
        """Fetches a dataset and stores it in the destination specified."""
        basedir=tools.get_base_dir()
        for d in self.data_list:
            os.system(basedir+"/scripts/ariadne-fetch.sh "+d+" "+destination)
            return 1


    def unpack(self, destination):
        """If the dataset is distributed as an archive, unpack the dataset in the
           destination specified.
        """
        if destination == "":
            destination = "."
        contents = os.listdir(destination)
        archive_plugins = get_plugins(PLUGIN_TYPE_ARCHIVE)
        for c in contents:
            ext = tools.get_extension(c)
            
            for a in archive_plugins:
                p=a[0]()
                if p.can_handle(ext):
                    p.unpack(destination+"/"+c, destination)
                return 1

    def get_file_list(self, destination):
        """Returns a list of all files in the dataset."""
        # This and get_file exist so that stages can get data for themselves.
        return os.listdir(destination)


    def get_file(self, destination, name, mode):
        """Returns a specific file in the dataset."""
        return open(destination+"/"+name, mode)


    def __init__(self, def_filename="", def_tokens=[]):
        return


class ArchivePlugin:
    """A plugin class intedned to wrap existing archive tools."""
    name=None
    
    
    def can_handle(self, extension):
        """Returns 1 if this plugin can handle the extension specified."""
        return 0
    
    
    def unpack(self, file_name, destination):
        """Unpacks the archive specified and stores its contents in the destination
           specified.
        """
        return
    
    
    def __init__(self):
        return


class AriadneOp:
    """A generic, top level interface for ariadne operations."""
    name=None


    def run(self, arg_dict):
        """Executes an operation using the args defined in arg_dict"""
        return 0


    def files_modified(self):
        """Returns a list of files modified by this plugin."""
        return []


    def get_arg_names(self):
        """Returns a list of argument names.
           These must be the same as the indices expected of run()'s arg_dict"""
        return []


    def depends(self):
        """Returns a list of DependencyContainers"""
        return []


    def test(self):
        """Executes any nose tests imported or defined in the plugin."""
        return nose.run()


    def __init__(self):
        return


class AriadneMLOp(AriadneOp):
    """Ariadne interface for machine learning stuff."""
    
    def benchmark(self, arg_dict):
        """Performs a benchmarking operation."""
        return


    def get_train_arg_names(self):
        """Returns a list of argument names to be used for the train() method."""
        return []


    def train(self, args):
        """Performs a training operation.
           This method is invoked in the same way as AriadneOp.run()"""
        return


    def train_depends(self):
        """Returns a list of DependencyContainers specific to the requirements
           of the train() method."""
        return []
