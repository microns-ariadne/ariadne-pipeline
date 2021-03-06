#!/usr/bin/env python
# This is a temporary version of ariadne as I change argument handling

#!/usr/bin/env python

import sys
import os
import ariadneplugin
import ariadnetools
import pipeline
import deftools
import argparse

# ariadne.py -- command line interface for ariadne.


def print_usage():
    print("Usage: ariadne.py <command> [args]")
    print("Manage, test, benchmark, and run software pipelines.")
    print("\nWhere <command> is one of the following:")
    print("\tdataset  \tManage, fetch, validate, and unpack datasets.")
    print("\ttest     \tRun tests on a pipeline.")
    print("\tbenchmark\tBenchmark a pipeline.")
    print("\tpipeline \tRun and manage pipelines.")
    print("\tplugins  \tList all available plugins.")


def print_dataset_usage():
    print("Usage: ariadne.py dataset <action> [datasetname] [destination]")
    print("\nWhere <action> is one of the following:")
    print("\tfetch\tFetch, unpack, and validate a dataset.")
    print("\tlist \tShow all known dataset definitions.")
    print("\tshow \tShow information about a datset.")


def print_pipeline_usage():
    print("Usage: ariadne.py pipeline <action> <pipelinename> [pipeline args]")
    print("\nWhere <action> is one of the following:")
    print("\trun         \tRun the pipeline.")
    print("\tcheckdepends\tEnsure that all of the pipeline's modules are present.")


def print_test_usage():
    print("Usage: ariadne.py test <pipelinename> <test definition file> [args]")


def print_benchmark_usage():
    print("Usage: ariadne.py benchmark <pipelinename> [pipeline args]")
    print("\nWhere [pipeline args] is a list of all arguments to send")
    print("\tto the pipeline.")


def build_arg_dict(arg_list):
    d={}
    for a in arg_list:
        toks=a.split('=')
        d[toks[0]]=toks[1]
    return d


def run_dataset(action, dataset_name):
    if action=="" and dataset_name=="":
        print_dataset_usage()
        return
    
    if action == "fetch":
        if not ariadnetools.file_exists(dataset_filename):
            print("ERROR: Dataset "+dataset_name+" does not exist.")
            return
        dataset_contents = deftools.parse_file(dataset_filename)
        dataset_type = deftools.search(dataset_contents, "type")[0]
        if len(dataset_type) == 0:
            print("ERROR: Dataset has unspecified type. Cannot handle.")
            exit(2)
        for hclass in dataset_handlers:
            h = hclass[0]()
            if h.can_handle(dataset_type):
                h=hclass[0](dataset_filename)
                h.fetch(dataset_destination)
                h.unpack(dataset_destination)

    elif action == "list":
        dirlisting=os.listdir('.')
        for entry in dirlisting:
            if ariadnetools.get_extension(entry) == ".dataset":
                print(entry.split('.')[0])

    elif action == "show":
        dataset_contents=deftools.parse_file(dataset_filename)
        dataset_type=deftools.search(dataset_contents, "type")[0]
        handler=None

        for hclass in dataset_handlers:
            h = hclass[0]()
            if h.can_handle(dataset_type):
                handler = h
                break

        print("Dataset: "+dataset_name)
        print("Type: "+deftools.search(dataset_contents, "type")[0])
        if handler == None:
            print("No plugin found to handle this type of dataset.")
        else:
            print("Handler plugin name: "+handler.name)
            
    else:
        print_dataset_usage()
        exit(0)


def run_plugins():
    print("List of plugins:")
    o = sys.stdout
    longest_len=0
    for p in ariadneplugin.plugin_list:
        if len(str(p[0].name)) > longest_len:
            longest_len=len(str(p[0].name))

    longest_len+=3

    o.write("Name")
    for i in range(0, longest_len-4, 1):
        o.write(" ")
    o.write("Type\n")

    for p in ariadneplugin.plugin_list:
        namedelta=longest_len-len(str(p[0].name))
        namestr=str(p[0].name)
        for i in range(0, namedelta, 1):
            namestr+=' '
        namestr+=p[1]+'\n'
        o.write(namestr)


def run_pipeline(action, pipe_name, args):
    if action == "run":
        pipe_args=build_arg_dict(args)
        p=pipeline.Pipeline(pipe_name+".pipeline")
        p.run(pipe_args)

    elif action=="checkdepends":
        p=pipeline.Pipeline(pipe_name+".pipeline")
        p.check_dependencies()


def run_test(pipe_name, test_filename):
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


def run_benchmark(pipe_name, args):
    if pipe_name=="":
        print_benchmark_usage()
        return
    pipe_name=args[0]
    argdict=build_arg_dict(args)
    
    p=pipeline.Pipeline(pipe_name+".pipeline")
    p.benchmark(argdict)


def run_plugin(plugin_name, plugin_args):
    if plugin_name="":
        print_run_plugin_usage()
        return
    pclass=ariadneplugin.search(plugin_name)
    argdict=build_arg_dict(plugin_args)
    pl=pclass(argdict)
    pl.run()


def main(argv):
    # These two are mostly for the benefit of plugins.
    sys.path.append(".")
    sys.path.append(ariadnetools.get_base_dir()+"/ariadne")
    ariadnetools.init_plugins()

    if len(argv) == 1:
        print_usage()
        exit()
        
    parser=argparse.ArgumentParser(description="Manage, test, and benchmark software pipelines.")
    parser.add_argument("cmd", help=argparse.SUPPRESS)
    parser.add_argument("optarg1", nargs="?")
    parser.add_argument("optarg2", nargs="?")
    parser.add_argument("moreargs", nargs="*")

    results=parser.parse_args()
    cmd=results.cmd
    if cmd == "dataset":
        run_dataset(results.optarg1, results.optarg2)
    elif cmd == "test":
        run_test(results.optarg1, results.optarg2)
    elif cmd == "benchmark":
        if results.optarg2!="":
            results.moreargs.append(results.optarg2)
        run_benchmark(results.optarg1, results.moreargs)
    elif cmd == "pipeline":
        run_pipeline(results.optarg1, results.optarg2, results.moreargs)
    elif cmd == "plugins":
        run_plugins()
    elif cmd == "runplugin":
        if results.optarg2!="":
            results.moreargs.append(results.optarg2)
        run_plugin(results.optarg1, results.moreargs)

if __name__ == "__main__":
    main(sys.argv)
