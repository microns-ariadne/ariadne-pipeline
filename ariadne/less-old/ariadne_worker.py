#!/usr/bin/env python

# ariadne_worker.py -- Defines a worker process for ariadne.

import os
import sys
import socket
import time
import multiprocessing
import ariadnetools
import ariadneplugin
import pipeline
import ariadne
import threading


def get_arg_dict(toks):
    ret_dict={}
    for t in toks:
        ttoks=t.split('=')
        ret_dict[ttoks[0]]=ttoks[1]
    return ret_dict


class ClientExecutor(threading.Thread):
    internal_plugin=None
    benchmode=0
    valmode=0
    cur_status="NA"


    def run(self):
        self.internal_plugin.run()
        if self.valmode:
            valresults=self.internal_plugin.validate()
            if valresults:
                print("PASS: "+internal_plugin.name)
            else:
                print("FAIL: "+internal_plugin.name)
        if self.benchmode:
            print("Executed in %f seconds." % self.internal_plugin.benchmark())
        if self.internal_plugin.success():
            self.cur_status="PASS"
        else:
            self.cur_status="FAIL"


    def __init__(self, plugin, benchmode, valmode):
        self.internal_plugin=plugin
        self.benchmode=benchmode
        self.valmode=valmode
        threading.Thread.__init__(self)


def run_client(i, o):
    line=i.readline()
    cur_thread=None
    validation_mode=0
    benchmark_mode=0


    try:
        while 1:
            print("Got: "+line)
            line=line.strip()
            linetoks=line.split()
            cmd=linetoks[0]
            if cmd=="loadcfg":
                ariadnetools.init_plugins(linetoks[1])
            elif cmd=="run":
                plugin_name=linetoks[1]
                argdict=get_arg_dict(linetoks[2:])
                print("Running plugin: "+plugin_name)
                pl_class=ariadneplugin.search_plugins(plugin_name)
                if pl_class==None:
                    print("ERROR: Could not find plugin.")
                else:
                    pl=pl_class(argdict)
                    
                    if cur_thread!=None:
                        if cur_thread.is_alive():
                            cur_thread.join()

                    cur_thread=ClientExecutor(pl, benchmark_mode, validation_mode)
                    cur_thread.start()
            elif cmd=="exit":
                exit(0)
            elif cmd=="valmode":
                validation_mode=not validation_mode
            elif cmd=="benchmode":
                benchmark_mode=not benchmark_mode
            elif cmd=="status":
                try:
                    if cur_thread.is_alive():
                        o.write("busy\n")
                        print("busy")
                    elif cur_thread.cur_status!="NA":
                        o.write(cur_thread.cur_status)
                    else:
                        o.write("ok\n")
                        print("ok")
                except:
                    o.write("ok\n")
                    print("ok")
                o.flush()
                
            line=i.readline().strip()  
    except:
        print("Worker exiting...")
    return


def spawn_workers():
    interface_list=[]
    procnum=multiprocessing.cpu_count()
    curpid=0
    i=None
    o=None
    
    pipelist=[]
    
    for i in range(0, procnum, 1):
        pin, cout=os.pipe()
        cin, pout=os.pipe()
        
        curpid=os.fork()
        if curpid == 0:
            os.close(pin)
            os.close(pout)
            i=os.fdopen(cin, "r")
            o=os.fdopen(cout, "w")
            #os.dup2(cin, sys.stdin.fileno())
            #os.dup2(cout, sys.stdout.fileno())
            break
        
        else:
            os.close(cin)
            os.close(cout)
            pin=os.fdopen(pin, "r")
            pout=os.fdopen(pout, "w")
            pipelist.append((pin, pout))
            
    if curpid!=0:
        return pipelist
    else:
        try:
            run_client(i, o)
        except:
            exit(1)
        exit(0)


def handle_query(query, pipeset, curworker, sock):
    print("Handling query.")
    qtoks=query.strip().split()
    i=pipeset[curworker][0]
    o=pipeset[curworker][1]
    o.write("status\n")
    o.flush()
    l=i.readline().strip()
    time.sleep(0.1)

    cmd=qtoks[0]
    print(cmd)
    print("query")
    print(query)
    print("status: "+l)
    if query==None:
        return 1

    if cmd=="run":
        if l=="busy":
            return 0
        o.write(query+"\n")
        o.flush()
    elif cmd=="loadcfg": # Issue to all workers:
        for p in pipeset:
            p[1].write(query+"\n")
            p[1].flush()
    elif cmd=="shutdown":
        sock.close()
        raise Exception
    elif cmd=="nop":
        print("Got alive-ness check from sender.")
    elif cmd=="wait":
        checkv=0
        while not checkv:
            checkv=1
            for p in pipeset:
                p[1].write("status\n")
                p[1].flush()
                l=p[0].readline().strip()
                checkv=checkv and l=="ok"
        sock.send("OK\n") #For synchronization.
    elif cmd=="benchmode" or cmd=="valmode":
        for p in pipeset:
            p[1].write(cmd+"\n")
            p[1].flush()
    else:
        print("Invalid command: "+query)

    sock.close()
    return 1


def run_controller():
    # Runs a very simple server service that is attached to a process pool.
    joblist=[]
    pipelist=spawn_workers()
    curworker=0
    
    ssock=socket.socket()
    ssock.bind(('127.0.0.1', 42424))
    
    try:
        ssock.listen(4)
        while 1:
            print("Accepting connection...")
            conn, addr=ssock.accept()
            try:
                query=conn.recv(1024)
                query=query.strip()
                print(query)
            
                while not handle_query(query, pipelist, curworker, conn):
                    print("Moving to next worker...")
                    curworker+=1
                    if curworker>(len(pipelist)-1):
                        curworker=0
            except socket.error:
                print("ERROR: Could not read socket data.")
    except Exception:
        print("Got exception. Exiting...")
        ssock.shutdown(socket.SHUT_RDWR)
        ssock.close()
        print("Shutting down workers...")
        for p in pipelist:
            p[1].write("exit\n")
            p[1].flush()
            p[1].close()
            p[0].close()
        

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
