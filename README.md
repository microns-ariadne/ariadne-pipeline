# ariadne-pipeline - Process and software pipeline management tool.

NOTE: ariadne-pipeline is still under development and testing. Overall behavior is mostly stable, but internal APIs and plugin specifications are subject to change.
Documentation valid for version 1.0a4

## The CLI
ariadne's core functions can be interacted with through ariadne.py:

Usage: ariadne.py <command> [args]
Manage, test, benchmark, and run software pipelines.

Where <command> is one of the following:
	dataset  	Manage, fetch, validate, and unpack datasets.
	test     	Run tests on a pipeline.
	benchmark	Benchmark a pipeline.
	pipeline 	Run and manage pipelines.
	plugins  	List all available plugins.

### ariadne dataset
This tool is used to fetch and prepare datasets for projects.
It is invoked in the following form:
`ariadne.py dataset <command> [dataset name]`
Where command may be one of the following:

* fetch -- Fetches the dataset named by [dataset name]
* list -- Prints all datasets defined in the current working directory.
* show -- Parses the dataset specified by [dataset name] and prints its contents.

The ariadne comes with a number of example datasets. These and any dataset definitions in the current directory can be interacted with through ariadne by specifying the name of the dataset without any file extensions, etc. 

### ariadne pipeline
Runs a pipeline. 

## Tutorials
This section contains a few tutorials that can help you familiarize yourself with ariadne and its behavior. 

### Ariadne machine learning tutorial
Ariadne is designed for use with machine learning pipelines. As such, its plugin architecture includes support for common machine learning tasks. This tutorial will cover how ariadne can be applied to a machine learning.

#### Setup
For this tutorial, you need to clone the following git repository:


`https://github.com/Rhoana/tensorflow-neuroproof-AC3.git`


This project has a number of dependencies that must be satisifed in order for it to execute correctly. These dependencies should be listed in the project's `dependencies.txt` 

#### Pipeline Design
Rather than just directly translating the pipeline as it is executed, it would be useful to consider how the pipeline runs and how much behavior is shared over the course of its execution. 

This is how the pipeline will be implemented in this tutorial:


make directories
train resnet
classify resnet
neuroproof learn/predict on training data
neuroproof predict


Each stage with dependencies will be passed the appropriate values so that each plugin can be reused as much as possible.

#### Writing plugins
This project is driven by a shell script that involves a large number of components. While it would be easy to just modify the script and run `shell2pipe` (as described in later tutorials), doing so would effectively just replace one format with a more complex one. This tutorial will present a mix of both approaches. All tasks not related to machine learning will be pushed to scripts or bulk plugins while machine learning tasks will be designed to take advantage of ariadne.


_Impatient?_ Just unpack ariadne-pipeline/examples/tensorflow-neuroproof-AC3.tar.gz in your cloned tensorflow project directory and skip to "Writing a Pipeline Definition File". Please note that the purpose of this tutorial is to demonstrate ariadne's design and usage in context.


Start by creating a plugins directory:

```
mkdir plugins
```

Now edit `plugins/ctrain.py`:

```python
import os
import plugin

plugin_class="ctrain"


class ctrain(plugin.AriadneOp):
    name="ctrain"

    def run(self, args):
        os.system("mkdir -p Workspace")
        os.system("$PYTHON $ROOT/util/create_input_datasets.py -i Data/ac3train/input -l Data/ac3train/labels -o Workspace/train_data.h5")
        os.system("$PYTHON $ROOT/util/create_membrane_training.py -i Workspace/train_data.h5 -p 5 -n 10")
```

The above plugin is taken more or less directly from the script and covers initial dataset creation. As such, there need not be much complexity in its specification. Also note that this example makes use of environment variables. These will be specified in the pipeline definition file.

Now edit `plugins/resnet.py`:

```python
import os
import plugin

plugin_class="resnet"


class resnet(plugin.AriadneMLOp):
    name="resnet"


    def depends(self):
        d=[]

        d.append(plugin.DependencyContainer("mkdir", {"dirname": "Workspace/checkpoints"}))
        d.append(plugin.DependencyContainer("mkdir", {"dirname": "Workspace/summaries"}))

        return d


    def get_train_arg_names(self):
        return ['numiters', 'learnrate', 'data']


    def train(self, args):
        numiters=1000
        learnrate=0.1
        data="train-data.h5"

        try:
            numiters=int(args['numiters'])
            learnrate=float(args['learnrate'])
            data=args['data']
        except:
            pass

        os.system("$PYTHON $ROOT/membrane_classifier/train_resnet.py --learning_rate %f --summary_dir Workspace/summaries --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/train_data.h5 --batch_size 3 --num_modules $RESNET_COUNT --iterations %d" % (learnrate, numiters))


    def get_arg_names(self):
        return ['data']


    def run(self, args):
        data="train_data.h5"

        try:
            data=args['data']
        except:
            pass

        os.system("$PYTHON $ROOT/membrane_classifier/classify_resnet.py --num_modules $RESNET_COUNT --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/%s" % data)
```

Note that this plugin extends AriadneMLOp. This allows it to integrate features that are useful to machine learning operations, such as the `train` method. 

The next plugin (`plugins/prepneuroproof.py`) is another that effectively just acts as a stage in the shell script:

```python
import os
import plugin

plugin_class="prepneuroproof"


class prepneuroproof(plugin.AriadneOp):
    name="prepneuroproof"


    def run(self, args):
        traintest="test"

        try:
            traintest=args['traintest']
        except:
            pass
        os.system($PYTHON $ROOT/util/prepare_neuroproof_training.py -i Workspace/%s_data.h5 -w Workspace/np_%s_watersheds.h5 -p Workspace/np_%s_probabilities.h5 -g Workspace/np_%s_groundtruth.h5" % (traintest, traintest, traintest, traintest))
```

Edit `plugins/watersheds.py`:
```python
import os
import plugin

plugin_class="watersheds"


class watersheds(plugin.AriadneOp):
    name="watersheds"


    def run(self, args):
        data="Workspace/test_data.h5"
        num=250

        try:
            data=args['data']
            num=int(args['num'])
        except:
            pass

        os.system("$PYTHON $ROOT/util/create_watersheds.py -i Workspace/%s -s %d" % (data, num))
```

This plugin makes use of the ability to specify arguments to each stage in the pipleline.

The following (`plugins/neuroproof.py`) wraps neuroproof functionality to produce a machine learning-specific plugin:

```python
import os
import plugin

plugin_class="neuroproof"


class neuroproof(plugin.AriadneMLOp):
    name="neuroproof"


    def train_depends(self):
        d=[]

        d.append(plugin.DependencyContainer("watersheds", {}))
        d.append(plugin.DependencyContainer("prepneuroproof", {}))
        return d

    def train(self, args):
        os.system("neuroproof_graph_learn Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/np_train_groundtruth.h5 --use_mito 0 --classifier-name Workspace/neuroproof_classifier.xml --num-iterations 1")

        os.system("neuroproof_graph_predict Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/neuroproof_classifier.xml --output-file Workspace/np_train_merged.h5")


    def depends(self):
        d=[]

        d.append(plugin.DependencyContainer("watersheds", {"data": "test_data.h5", "num": "250"}))
        d.append(plugin.DependencyContainer("prepneuroproof", {"traintest": "test"}))


    def run(self, args):
        os.system("neuroproof_graph_predict Workspace/np_test_watersheds.h5 Workspace/np_test_probabilities.h5 Workspace/neuroproof_classifier.xml --output-file Workspace/np_test_merged.h5")
```

#### Writing a plugin list file
In order for ariadne to be able to read and use the plugins written in the previous step, it is necessary to write a brief file naming each plugin.

Edit `plugins/plugins.list` as follows:

```
AriadneOp ctrain
AriadneOp watersheds
AriadneOp prepneuroproof
AriadneMLOp 
AriadneMLOp neuroproof

#### Writing a pipeline definition file
In order to accomodate the large number of possible configurations that each pipeline stage may need, pipleine definition files are formatted differently from other definition files. 

Edit `tutorial.pipeline` as follows:
```
name:
    tutorial
end

description:
    Tutorial pipeline.
end

plugindir:
    plugins
end

stages:
    ctrain:
        plugin: ctrain
        runtype: run
    end

    resnet1:
        plugin: resnet
        runtype: train
    end

    resnet2:
        plugin: resnet
        runtype: run
    end

    nproof1:
        plugin: neuroproof
        runtype: train
    end

    nproof2:
        plugin: neuroproof
        runtype: run
    end
end

environment:
    ROOT=/path/to/your/tensorflow-neuroproof-AC3
    PYTHON=/path/to/your/python
    LD_LIBRARY_PATH=/usr/local/cuda/lib64
    PATH=/path/to/your/neuroproof/build/environment/bin
    RESNET_COUNT=25
end
```

Each stage is expected to have a unique name that can be imported as a `python` module. This name need not be the same as the plugin it calls. Please note that the pipeline's environment variables are incomplete and should be filled in to match your specific setup.  


#### Running the pipeline

In order to run the pipeline, use the following command:


```
ariadne.py pipeline run tutorial
```

You may want to redirect output to a file so that it can be analyzed later.


### Shell Script Conversion Tutorial
This tutorial is the easiest, and demonstrates some of the potential uses of ariadne conversion in existing environments.

In this tutorial, you will:
1. Convert a shell script to an ariadne pipeline.
2. Execute the pipeline.
3. Examine the outputs and results of the execution task.

#### Creating a shell script.
Start by creating an empty directory for a demo project and its scripts. Then, using your favorite editor, enter the following and save it as `tutorial.sh`:

```bash
# mkdirs
mkdir a
mkdir b

# write_file
echo "test" >> a/test.txt

# create_output
cp a/test.txt b/foo.txt
```

This script is formatted for a tool included by ariadne named `shell2pipe.py`. `shell2pipe` can be used to convert specially formatted shell scripts to complete ariadne pipelines. The limitations imposed by shell2pipe are as follows:

* Each comment (excluding a shell specifier) specifies the name of a pipeline stage/plugin. There can thus be no spaces in comments.
* Each line can be executed by an independent call to os.system()
* All environment declarations are in the form: `export MYENV=value`
* All environment declarations, if possible, can be appended to the existing value of that environment variable. (ie. `export PATH=:/my/path` would be executed as `export PATH=$PATH:/my/path`
* Each group of lines between comments can be executed sequentially in the same plugin.

Given that it follows these guidelines, any shell script could likely be converted by `shell2pipe`.

#### Generating a pipeline
Once you have finished writing the script, run the following:

```
shell2pipe.py tutorial.sh plugins tutorial
```

If you check the contents of the current directory, you should see that shell2pipe has created a plugins directory (in this case, `plugins`) and a pipeline definition file (`tutorial.pipeline`).

#### Executing the pipeline
To run the pipeline you just generated, run the following:

```
ariadne.py pipeline run tutorial
```

If everything is configured properly, you should see a large volume of text from `luigi` indicating that it has successfully executed each generated pipeline stage in order. You should also see a number of python files named after each plugin that was generated in the previous step.

#### Analyzing the results
Now that execution has completed and ariadne had generated a number of python modules, it may be helpful to look through them.

First, look at the contents of `plugins/mkdirs.py`. It should look something like the following:

```python
# generated by shell2pipe on 2016-03-18
import os
import plugin

plugin_class='mkdirs'


class mkdirs(plugin.AriadneOp):
    name='mkdirs'


    def run(self, args):
        os.system('mkdir a')
        os.system('mkdir b')
```

Here you can see the four main elements that make up a minimal airande execution plugin:


* Appropriate module imports -- in this case plugin (which defines a number of base classes and utility functions for ariadne plugins) and os.

* The plugin_class attribute -- this tells ariadne's plugin loader which class within the module to load and treat as a plugin. This allows developers to include additional classes if necessary.

* The plugin class and name definition -- Note that the plugin defined here extends AriadneOp, which is detailed in the API section of this document. It also declares a name for itself. While this is currently expected to be the same as the plugin's class name, future revisions of ariadne may remove this attribute as it is currently rarely useful.

* The `run` method -- This is the actual execution portion of the plugin. It is expected that the `run` method can accept a dictionary of arguments, though in this case it is being used merely as a script for external programs.

Now open one of the automatically generated luigi modules in the base directory of the project. Here is an example:

```python
# Generated by ariadne on 2016-03-18.
import luigi
import os
class mkdirs_l(luigi.Task):
    def requires(self):
        return
    def run(self):
        os.system('ariadne.py runplugin mkdirs plugins')
```

Here you can see how `luigi` is used to execute and manage ariadne plugins. It can both call ariadne to execute plugins and generate a dependency tree for each pipeline stage.
    
## Execution model

Ariadne's execution process is ultimately comprised of four stages:
1. Pipeline analysis
2. Pipeline compilation
3. Luigi execution
4. Ariadne plugin execution.

### 1. Pipeline analysis
In this stage, ariadne determines which stages comprise a pipeline, the order they are executed in, and whether they depend on one or more plugins. During this stage, ariadne also installs all environment variables specified in the pipeline definition file.

### 2. Pipeline compilation
Once ariadne has completed its analysis of the pipline, it generates a luigi wrapper for each pipeline stage. This wrapper is designed to execute ariadne instances that, in turn, execute the individual plugins specified by the pipeline and its dependencies.

### 3. Luigi execution
Ariadne proceeds to call luigi and execute each pipeline stage in order.

### 4. Ariadne plugin execution.
Luigi, in executing each generated plugin, runs an ariadne instance that handles the execution of that specific plugin and exits. This process takes advantage of the fact that luigi can do automatic dependency checks and resolution, as each dependency is wrapped in the luigi module. 

## Definition file format

Each definition file follows a simple format:

```
key_name:
    key_value
```


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
* `parallel` -- Whether the plugin can be run in parallel. In future releases, it will be assumed that all tasks can be validated and benchmarked without internal state.

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
