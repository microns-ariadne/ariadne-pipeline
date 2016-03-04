#!/usr/bin/env python

# ariadne-benchmark.py -- Benchmarks a pipeline using its validation arguments.
import ariadnetools
import os
import sys
import Pipeline
import time
import cpuinfo # py-cpuinfo

def printUsage():
    print("Usage: ariadne-benchmark.py <pipeline> [args]")
    print("Benchmark a pipeline.")
    print("\nWhere args may be one or more of the following:")
    print("\t--logfile=<filename>\tSpecifies a file to write benchmarking output to.")
    print("\t--benchmark=<benchname>\tSpecifies which benchmark to run (if possible)")
    print("\t--list-benchmarks\tLists all benchmarks in the pipeline.")

def runBenchmark(pipename, benchmarkSetName, logFileName):
    p=Pipeline.Pipeline(pipename+".pipeline")

    # Determine the benchmark's index:
    index=-1
    for i in range(0, len(p.benchmarks), 1):
        if p.benchmarks[i][0]==benchmarkSetName:
            index=i

    if index==-1:
        print("Error: benchmark not found.")

    startTime=time.time()
    p.executePipe(p.benchmarks[index][1:])
    totalTime=time.time-startTime

    print("Benchmark run took "+str(totalTime)+" seconds.")
    
    logFile=None
    if logFileName=="":
        logFile=sys.stdout
    else:
        logFile=open(logFileName, 'w')

    logFile.write("Total benchmark time: "+str(totalTime)+" seconds\n")
    logFile.write("System information:")

    info=cpuinfo.get_cpu_info()

    logFile.write("CPU make: "+info['vendor_id']+"\n")
    logFile.write("CPU model: "+info['brand']+"\n")
    # TODO: Insert more information.
    logFile.close()

def listBenchmarks(pipename):
    p=Pipeline.Pipeline(pipename+".pipeline")

    print("List of benchmarks:")

    for b in p.benchmarks:
        print(b[0])

if len(sys.argv)==1:
    printUsage()

pipelineName=sys.argv[1]
logFile=""
benchmarkName=""

for arg in sys.argv[1:]:
    argToks=arg.split('=')
    if argToks[0]=="--logfile":
        if len(argToks)==1:
            print("Error: no log file name specified.")
            print("Try --logfile=filename")
        logFile=argToks[1]
    elif argToks[0]=="--benchmark":
        benchmarkName=argToks[1]
    elif argToks[0]=="--list-benchmarks":
        listBenchmarks(pipelineName)
        exit(0)

runBenchmark(pipelineName, benchmarkName, logFile)
