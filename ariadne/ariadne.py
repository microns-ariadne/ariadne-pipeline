#!/usr/bin/env python
# This is a temporary version of ariadne as I change argument handling

import sys
import os
import plugin
import tools
import pipeline
import deftools
import argparse

# ariadne.py -- command line interface for ariadne.


def print_usage():
    """Prints a general usage statement for ariadne."""
    print("Usage: ariadne.py <command> [args]")
    print("Manage, test, benchmark, and run software pipelines.")
    print("\nWhere <command> is one of the following:")
    print("\tdataset  \tManage, fetch, validate, and unpack datasets.")
    print("\ttest     \tRun tests on a pipeline.")
    print("\tbenchmark\tBenchmark a pipeline.")
    print("\tpipeline \tRun and manage pipelines.")
    print("\tplugins  \tList all available plugins.")


def print_dataset_usage():
    """Prints a usage statement for the dataset component of ariadne."""
    print("Usage: ariadne.py dataset <action> [datasetname] [destination]")
    print("\nWhere <action> is one of the following:")
    print("\tfetch\tFetch, unpack, and validate a dataset.")
    print("\tlist \tShow all known dataset definitions.")
    print("\tshow \tShow information about a datset.")


def print_pipeline_usage():
    """Prints a usage statement for the pipeline component of ariadne."""
    print("Usage: ariadne.py pipeline <action> <pipelinename> [pipeline args]")
    print("\nWhere <action> is one of the following:")
    print("\trun         \tRun the pipeline.")
    print("\tcheckdepends\tEnsure that all of the pipeline's modules are present.")


def print_test_usage():
    """Prints a usage statement for the test component of ariadne."""
    print("Usage: ariadne.py test <pipelinename> <test definition file> [args]")


def print_benchmark_usage():
    """Prints a usage statement for the benchmark component of ariadne."""
    print("Usage: ariadne.py benchmark <pipelinename> [pipeline args]")
    print("\nWhere [pipeline args] is a list of all arguments to send")
    print("\tto the pipeline.")


def build_arg_dict(arg_list):
    """Builds a dictionary from an argument listing."""
    d={}
    for a in arg_list:
        toks=a.split('=')
        d[toks[0]]=toks[1]
    return d


def list_datasets(path):
    """Lists information for all datasets present in the given path."""
    dirlisting=os.listdir(path)
    for entry in dirlisting:
        if tools.get_extension(entry)==".dataset":
            dataset_contents=deftools.parse_file(path+"/"+entry)
            ds_name=""
            ds_descrip=""
            try:
                ds_name=deftools.search(dataset_contents, "name")[0]
            except:
                ds_name="None"
            try:
                ds_descrip=deftools.search(dataset_contents, "description")[0]
            except:
                ds_descrip="No description found."
            print("%s: %s" % (ds_name, ds_descrip))
            

def run_dataset(action, dataset_name, confdict):
    """Performs actions related to fetching, unpacking, and managing datasets."""
    if action=="" and dataset_name=="":
        print_dataset_usage()
        return

    dataset_destination=confdict['datadir'][0]

    # Determine where, exactly, this dataset is:
    fullpath="%s/%s.dataset" % (tools.get_default_dataset_dir(), dataset_name)
    if not tools.file_exists(fullpath):
        fullpath="./%s.dataset" % dataset_name

    dataset_filename=fullpath

    if action=="fetch":
        if not tools.file_exists(fullpath):
            print("ERROR: Dataset "+dataset_name+" does not exist either in ./ or %s." 
                    % tools.get_default_dataset_dir())
            return
        dataset_contents = deftools.parse_file(dataset_filename)
        dataset_type = deftools.search(dataset_contents, "type")[0]
        if len(dataset_type) == 0:
            print("ERROR: Dataset has unspecified type. Cannot handle.")
            exit(2)

        dataset_handler=plugin.get_can_handle(dataset_type)

        if dataset_handler==None:
            print("Could not find a plugin to handle dataset type: %s" % dataset_type)
            return

        h=dataset_handler(dataset_filename)
        h.fetch(dataset_destination)
        h.unpack(dataset_destination)

    elif action == "list":
        list_datasets(tools.get_default_dataset_dir())
        list_datasets(".")

    elif action == "show":
        if not tools.file_exists(fullpath):
            print("ERROR: Dataset %s does not exist." % dataset_name)
            return
        dataset_contents=deftools.parse_file(fullpath)
        dataset_type=deftools.search(dataset_contents, "type")[0]
        handler=None
        dataset_handler=plugin.get_can_handle(dataset_type)

        print("Dataset: "+dataset_name)
        print("Type: "+deftools.search(dataset_contents, "type")[0])
        if dataset_handler == None:
            print("No plugin found to handle this type of dataset.")
        else:
            print("Handler plugin name: "+dataset_handler.name)
            
    else:
        print_dataset_usage()
        exit(0)


def run_plugins():
    """Lists all currently installed plugins."""
    print("List of plugins:")
    o = sys.stdout
    longest_len=0
    for p in plugin.plugin_list:
        if len(str(p[0].name)) > longest_len:
            longest_len=len(str(p[0].name))

    longest_len+=3

    o.write("Name")
    for i in range(0, longest_len-4, 1):
        o.write(" ")
    o.write("Type\n")

    for p in plugin.plugin_list:
        namedelta=longest_len-len(str(p[0].name))
        namestr=str(p[0].name)
        for i in range(0, namedelta, 1):
            namestr+=' '
        namestr+=p[1]+'\n'
        o.write(namestr)


def run_pipeline(action, pipe_name, args, confdict):
    """Performs actions related to running and managing pipelines."""
    if action == "run":
        pipe_args=build_arg_dict(args)
        p=pipeline.Pipeline(pipe_name+".pipeline")
        p.run(pipe_args)

    elif action=="checkdepends":
        p=pipeline.Pipeline(pipe_name+".pipeline")
        p.check_dependencies()


def run_test(pipe_name, test_filename, confdict):
    """Performs actions related to testing plugins and pipelines."""
    if pipe_name=="" or test_filename=="":
        print_test_usage()
        return
    
    f=open(test_filename, 'r')
    contents=f.read()
    f.close()
    
    lines=contents.splitlines()
    arglist=[]
    
    for l in lines:
        linetoks=l.split()
        name=linetoks[0]
        argdict={'test_name': name}
        for t in linetoks[1:]:
            pair=t.split('=')
            argdict[pair[0]]=pair[1]
            print(argdict)
        arglist.append(argdict)

    p=pipeline.Pipeline(pipe_name+".pipeline")
    p.validate(arglist, step)


def run_benchmark(pipe_name, args, confdict):
    """Performs actions related to benchmarking plugins and pipelines."""
    if pipe_name=="":
        print_benchmark_usage()
        return
    pipe_name=args[0]
    argdict=build_arg_dict(args)
    
    p=pipeline.Pipeline(pipe_name+".pipeline")
    p.benchmark(argdict)


def run_plugin(runstr, plugin_name, plugin_dir, plugin_args, confdict):
    """Runs an individual plugin by the method specified."""
    if plugin_name=="":
        print_run_plugin_usage()
        return
    tools.init_plugins(plugin_dir)
    pclass=plugin.search_plugins(plugin_name)
    if pclass==None:
        print("ERROR: Plugin %s could not be found!" % plugin_name)
        return
    argdict=build_arg_dict(plugin_args)
    pl=pclass()
    if runstr=="runplugin":
        pl.run(argdict)
    elif runstr=="trainplugin":
        try:
            pl.train(argdict)
        except:
            print("ERROR: Couldn't train plugin: %s" % plugin_name)
    elif runstr=="testplugin":
        retv=0

        try:
            retv=pl.test()
        except:
            print("ERROR: Couldn't test plugin: %s" % plugin_name)

        exit(not retv)

def main(argv):
    """Entry point and dispatcher for the ariadne cli."""
    # These two are mostly for the benefit of plugins.
    sys.path.append(".")
    sys.path.append(tools.get_base_dir()+"/ariadne")
    tools.init_plugins()

    if len(argv) == 1:
        print_usage()
        exit()

    # Now attempt to read the configuration file:
    conftoks=[]
    try:
        conftoks=deftools.parse_file(tools.get_default_config_file())
    except:
        # Try to write one instead:
        print("Generating default config file at %s..." % (tools.get_default_config_file()))
        conffile=open(tools.get_default_config_file(), 'w')
        tools.prep_default_config_file(conffile)
        conffile.close()
        conftoks=tools.get_default_conf_toks()

    confdict=deftools.make_dict(conftoks)
    plugin.set_config(confdict)

    # Load any plugins specified in the configuration:
    try:
        pdirs=confdict['plugindirs']
        for p in pdirs:
            tools.init_plugins(p)
            print("Loaded plugins from: %s" % p)
    except:
        pass

    parser=argparse.ArgumentParser(description="Manage, test, and benchmark software pipelines.")
    parser.add_argument("cmd", help=argparse.SUPPRESS)
    parser.add_argument("optarg1", nargs="?")
    parser.add_argument("optarg2", nargs="?")
    parser.add_argument("moreargs", nargs="*")

    results=parser.parse_args()
    cmd=results.cmd
    if cmd == "dataset":
        run_dataset(results.optarg1, results.optarg2, confdict)
    elif cmd == "test":
        run_test(results.optarg1, results.optarg2, confdict)
    elif cmd == "benchmark":
        if results.optarg2!="":
            results.moreargs.append(results.optarg2)
        run_benchmark(results.optarg1, results.moreargs, confdict)
    elif cmd == "pipeline":
        run_pipeline(results.optarg1, results.optarg2, results.moreargs, confdict)
    elif cmd == "plugins":
        run_plugins()
    elif cmd == "runplugin" or cmd == "trainplugin":
        run_plugin(cmd, results.optarg1, results.optarg2, results.moreargs, confdict)


if __name__ == "__main__":
    main(sys.argv)
