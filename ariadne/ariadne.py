#!/usr/bin/env python

import sys
import os
import ariadneplugin
import ariadnetools
import pipeline
import deftools

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
    print("Where <action> is one of the following:")
    print("\trun         \tRun the pipeline.")
    print("\tcheckdepends\tEnsure that all of the pipeline's modules are present.")


def run_dataset(args):
    if len(args) == 0:
        print_dataset_usage()
        exit(1)
    
    action=args[0]
    dataset_name=""
    if len(args)>1:
        dataset_name=args[1]

    dataset_destination=""
    if len(args)>2:
        dataset_destination=args[2]

    dataset_filename=dataset_name+".dataset"
    dataset_handlers=ariadneplugin.get_plugins(ariadneplugin.PLUGIN_TYPE_DATASET)
    
    if action == "fetch":
        if not ariadnetools.file_exists(dataset_filename):
            print("ERROR: Dataset "+dataset_name+" does not exist.")
            return
        dataset_contents=deftools.parse_file(dataset_filename)
        dataset_type=deftools.search(dataset_contents, "type")[0]
        if len(dataset_type)==0:
            print("ERROR: Dataset has unspecified type. Cannot handle.")
            exit(2)
        for hclass in dataset_handlers:
            h=hclass[0]()
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
            h=hclass[0]()
            if h.can_handle(dataset_type):
                handler=h
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


def run_plugins(args):
    print("List of plugins:")
    print("Name\tType")
    for p in ariadneplugin.plugin_list:
        print(str(p[0].name)+"\t"+p[1])


def run_pipeline(args):
    if len(args)<2:
        print_pipeline_usage()
        return
    
    action=args[0]
    pipe_name=args[1]
    
    if action == "run":
        pipe_args={}
        for a in args[2:]:
            toks=a.split('=')
            pipe_args[toks[0].strip('-')]=toks[1]
        p=pipeline.Pipeline(pipe_name+".pipeline", pipe_args)
        p.run()
        
        
def main(argv):
    # These two are mostly for the benefit of plugins.
    sys.path.append(".")
    sys.path.append(ariadnetools.get_base_dir()+"ariadne")
    ariadnetools.init_plugins()

    if len(argv) == 1:
        print_usage()
        exit()

    if argv[1] == "dataset":
        run_dataset(argv[2:])
    elif argv[1] == "test":
        run_test(argv[2:])
    elif argv[1] == "benchmark":
        run_benchmark(argv[2:])
    elif argv[1] == "pipeline":
        run_pipeline(argv[2:])
    elif argv[1] == "plugins":
        run_plugins(argv[2:])
    for a in argv:
        toks = a.split()

if __name__ == "__main__":
    main(sys.argv)
