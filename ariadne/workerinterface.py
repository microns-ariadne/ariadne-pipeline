# workerinterface.py -- Functions to interact with worker controller processes on (potentially)
# remote systems.
import os
import sys
import socket
import threading
import ariadnetools

class worker_instance:
    pid=0
    hostname=""
    port=0


    def __init__(self):
        return


local_worker_instance=None


def getsock(inst):
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    return s, retv


def loadconfig(inst, config_dir):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect(inst.hostname, inst.port)
    
    if not retv:
        print("WARNING: Could not send plugin read command to worker instance.")
    else:
        s.send("loadcfg "+config_dir+"\n")
        s.close()


def loadconfig_local(config_dir):
    loadconfig(local_worker_instance, config_dir)


def disconnect_instance(inst):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    
    if not retv:
        print("WARNING: Couldn't connect to instance for shutdown.")
    else:
        s.send("shutdown\n")
        s.close()


def disconnect_local():
    disconnect_instance(local_worker_instance)
    local_worker_instance=None


def run(inst, plugin_name, args):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    
    if not retv:
        print("WARNING: Could not connect to instance!")
    else:
        send_str="run "
        send_str+=plugin_name
        for k in args:
            send_str+=" "+k
            send_str+="="+args[k]
        send_str+="\n"
        
        s.send(send_str)
        s.close()


def run_local(plugin_name, args):
    run(local_worker_instance, plugin_name, args)


def wait(inst):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))

    if not retv:
        print("WARNING: Could not wait for instance!")
    else:
        s.write("wait\n")
        s.recv(1024)
        s.close()


def wait_local():
    wait(local_worker_instance)


def validate(inst):
    if inst==None:
        return
    s, err=getsock(inst)

    if not err:
        print("WARNING: Could not toggle validation.")
    else:
        s.write("valmode\n")
        s.close()


def validate_local():
    validate(local_worker_instance)


def benchmarking(inst):
    if inst==None:
        return
    s, err=getsock(inst)

    if not err:
        print("WARNING: Could not toggle benchmarking.")
    else:
        s.write("benchmode\n")
        s.close()


def benchmarking_local():
    benchmarking(local_worker_instance)


def connect_local():
    if 1:#local_worker_instance==None:
        local_worker_instance=worker_instance()
        local_worker_instance.pid=os.spawnlp(os.P_NOWAIT, ariadnetools.get_base_dir()+"/ariande/ariadne_worker.py", "ariadne_worker.py", "controller")
        local_worker_instance.port=42424
        local_worker_instance.hostname="127.0.0.1"
        loadconfig_local(ariadnetools.get_base_dir()+"/plugins")
    return local_worker_instance


def init():
    local_worker_instance=None
