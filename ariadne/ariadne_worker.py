#!/usr/bin/env python

# ariadne_worker.py -- Defines a worker process for ariadne.

import os
import sys
import socket
import multiprocessing
import ariadnetools
import ariadneplugin
import pipeline


def get_arg_dict(toks):
    ret_dict={}
    for t in toks:
        ttoks=t.split('=')
        ret_dict[ttoks[0]]=ttoks[1]
    return ret_dict


def run_client():
    print("Hello, there.")
    i=sys.stdin
    o=sys.stdout
    line=i.readline().strip()
    while line != "":
        print("Client line: "+line)
        line=line.strip()
        linetoks=line.split()
        cmd=linetoks[0]
        if cmd=="loadfrom":
            ariadnetools.init_plugins(cmd)
        elif cmd=="run":
            plugin_name=linetoks[1]
            argdict=get_arg_dict(linetoks[2:])
            pl_class=ariadneplugin.search_plugins(plugin_name)
            pl=pl_class(argdict)
            pl.run()
        elif cmd=="exit":
            print("Exiting...")
            exit(0)
        elif cmd=="status":
            print("OK")
        line=i.readline().strip()
            
    return


def spawn_workers():
    interface_list=[]
    procnum=multiprocessing.cpu_count()
    curpid=0
    
    pipelist=[]
    
    for i in range(0, procnum, 1):
        pin, cout=os.pipe()
        cin, pout=os.pipe()
        
        curpid=os.fork()
        if curpid == 0:
            os.close(pin)
            os.close(pout)
            os.dup2(cin, sys.stdin.fileno())
            #os.dup2(cout, sys.stdout.fileno())
            break
        
        else:
            os.close(cin)
            os.close(cout)
            pipelist.append((pin, pout))
            
    if curpid!=0:
        return pipelist
    else:
        try:
            run_client()
        except:
            exit(1)
        exit(0)


def handle_query(query, pipeset):
    return


def run_controller():
    # Runs a very simple server service that is attached to a process pool.
    pipelist=spawn_workers()
    curworker=0
    
    ssock=socket.socket()
    ssock.bind(('127.0.0.1', 9000))
    
    try:
        ssock.listen(1)
        while 1:
            print("Accepting connection...")
            conn, addr=ssock.accept()
            conn.send("CMD?\n")
            query=conn.recv(1024)
            query=query.strip()
            conn.close()
            print(query)
            handle_query(query, pipelist[curworker])
            curworker+=1
            if curworker>(len(pipelist)-1):
                curworker=0
    except KeyboardInterrupt:
        print("Got keyboard interrupt. Exiting...")
    ssock.close()
    print("Shutting down workers...")
    for p in pipelist:
        os.write(p[1], "exit\n")
        os.close(p[1])
        os.close(p[0])
        

def main(args):
    i=sys.stdin
    o=sys.stdout
    
    if len(args)!=1:
        if args[1]=="controller":
            run_controller()
            return
            
    
    # Runs while the input isn't EOF.
    """
    while (line=i.readline()) != "":
        line=line.strip()
        linetoks=line.split()
        cmd=linetoks[0]
        if cmd=="loadfrom":
            ariadnetools.init_plugins(cmd)
        elif cmd=="run":
            plugin_name=linetoks[1]
            argdict=get_arg_dict(linetoks[2:])
            pl_class=ariadneplugin.search_plugins(plugin_name)
            pl=pl_class(argdict)
            pl.run()
    """
    
if __name__ == "__main__":
    main(sys.argv)