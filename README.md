# ariadne-pipeline - Process and software pipeline management tool.

NOTE: ariadne-pipeline is still under development and testing. Overall behavior is mostly stable, but internal APIs and plugin specifications are subject to change.

## Plugin API

Ariadne is ultimately a coordinator for a large number of plugins. As such, it is often necessary to develop new plugins to design different pipelines or just to fit different needs. 

Presently, there are three plugin interfaces:
1. ariadneplugin.Plugin -- A generic executable plugin designed as a building block for pipelines.
2. ariadneplugin.DatasetPlugin -- A plugin intended to wrap and abstract various dataset operations.
3. ariadneplugin.ArchivePlugin -- A plugin that wraps an archive utility.

Every module must have the following attributes:
* `project_class` -- The name of the plugin's class.
* A plugin definition that extends one of the interfaces listed above.

###ariadneplugin.Plugin
This interface must contain, at a minimum, the following:

* `name` -- A string containing the plugin's name. This need not be the same as its class name.

All other methods exist to provide the plugin with flexibility and functionality.

List of methods:

* `run(self)` -- This contains the main execution logic of the plugin.
* `depends(self)` -- This generates a list of DependencyContainer objects that specify all of the tasks that the plugin may depend on in order to execute correctly.
* `success(self)` -- Returns either True or False depending on whether the plugin was able to execute.
* `validate(self)` -- This is used to determine whether the plugin was able to pass internal tests under certain circumstances.
* `check_inputs(self)` -- Unused.
* `benchmark(self)` -- Returns the time taken to execute the plugin. All other metrics should be accounted for and logged by the plugin itself. 
* `__init__(self, args={}, conffile="", conftoks=[])` -- Used to parse arguments, initialize the plugin, and otherwise ensure that it is in a usable state. If all three inputs are left with their default values, it is expected that this method immediately return. 


###ariadneplugin.DatasetPlugin
This interface must contain, at a minimum, the following:

* `name` -- A string containing the plugin's name. This need not be the same as its class name.

The DatasetPlugin class already has logic to handle several use cases. If this existing logic is to be used, the following should be set in the class' constructor:

* `data_list` -- A list of strings representing URLs to be fetched and unpacked.

List of methods:

* `can_handle(self, ext)` -- Returns either True or False depending on whether the plugin can handle the specified dataset type. Dataset types should be written in the form: "dataset/type". For example, the included HDF5 plugin can handle datasets of type "dataset/hdf5"
* `validate(self)` -- Returns either True or False depending on whether the dataset could be fetched.
* `fetch(self, destination)` -- This method is already implemented by default. In its stock form, it will fetch all of the data referred to by `data_list` and store the files in the directory referred to by `destination`. This method may be overridden if different behavior is necessary.
* `unpack(self, destination)` -- This method is already implemented by default. In its stock form, it will list all files in the destination directory, search for archive plugins, and try to unpack as much as it can. This method may be overridden if different behavior is necessary.
* `get_file_list(self, destination)` -- This method is already implemented by default. In its stock form, it will return a directory listing for `destination`. This method may be overridden if necessary.
* `get_file(self, destination, name, mode)` -- This method is already implemented by default. In its stock form, it will return a file opened with the mode specified. This method allows datasets to be specified in abstract formats, given that they use some sort of object-oriented interface.
* `__init__(self, def_filename="", def_tokens=[])` -- Used to parse dataset definition files and do initialization. If all inputs are left with their default values, it is expected that this method immediately return.


###ariadneplugin.ArchivePlugin
This interface must contain, at a minimum, the following:

* `name` -- A string containing the plugin's name. This need not be the same as its class name.

The ArchivePlugin interface is very compact. 

List of methods:
* `can_handle(self, extension)` -- Returns True or False depending on whether the plugin can handle the specified extension. For example, the targz plugin can handle ".tar.gz" or ".tgz" archives.
* `unpack(self, file_name, destination)` -- Should unpack the specified file and put the resulting data in destination.
* `__init__(self)` -- Need not be overriden.


###ariadneplugin.DependencyContainer
This class is used by the Plugin interface to define various execution dependencies.

List of attributes:
* `dependency_name` -- The name of a plugin. The current set of plugins will be searched for this name on execution.
* `arg_dict` -- A dictionary of arguments to pass to the plugin.

It shouldn't be neccessary in normal use to directly use the above attributes. Instead, they should be specified with the DependencyContainer class' constructor:

`__init__(self, depname, args)`
