# workerinterface.py -- Functions to interact with worker controller processes on (potentially)
# remote systems.
import os
import sys
import socket
import threading
import ariadnetools

class WorkerInstance:
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
        print("Instance null for some reason.")
        return
    print("Hostname, port: "+str((inst.hostname, inst.port)))
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    
    if retv:
        print("WARNING: Could not send plugin read command to worker instance.")
    else:
        s.send("loadcfg "+config_dir+"\n")
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def loadconfig_local(config_dir):
    global local_worker_instance
    loadconfig(local_worker_instance, config_dir)


def shutdown_instance(inst):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    
    if retv:
        print("WARNING: Couldn't connect to instance for shutdown.")
    else:
        s.send("shutdown\n")
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def disconnect_local():
    global local_worker_instance
    # If we actually spawned the worker process. Otherwise, it's probably there for debugging, etc.
    if local_worker_instance.pid != 0:
        shutdown_instance(local_worker_instance)
    local_worker_instance=None


def run(inst, plugin_name, args):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))
    
    if retv:
        print("WARNING: Could not connect to instance!")
    else:
        send_str="run "
        send_str+=plugin_name
        for k in args:
            send_str+=" "+k
            send_str+="="+args[k]
        send_str+="\n"
        
        s.send(send_str)
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def run_local(plugin_name, args):
    global local_worker_instance
    run(local_worker_instance, plugin_name, args)


def wait(inst):
    if inst==None:
        return
    s=socket.socket()
    retv=s.connect((inst.hostname, inst.port))

    if retv:
        print("WARNING: Could not wait for instance!")
    else:
        s.send("wait\n")
        s.recv(1024)
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def wait_local():
    global local_worker_instance
    wait(local_worker_instance)


def validate(inst):
    if inst==None:
        return
    s, err=getsock(inst)

    if not err:
        print("WARNING: Could not toggle validation.")
    else:
        s.send("valmode\n")
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def validate_local():
    global local_worker_instance
    validate(local_worker_instance)


def benchmarking(inst):
    if inst==None:
        return
    s, err=getsock(inst)

    if not err:
        print("WARNING: Could not toggle benchmarking.")
    else:
        s.send("benchmode\n")
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def benchmarking_local():
    global local_worker_instance
    benchmarking(local_worker_instance)


def test_local_running():
    s=socket.socket()
    try:
        s.connect(('127.0.0.1', 42424))
        s.send("nop\n")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return 1
    except:
        return 0


def connect_local():
    global local_worker_instance
    if local_worker_instance==None:
        local_worker_instance=WorkerInstance()
        if test_local_running():
            local_worker_instance.pid=0
        else:
            local_worker_instance.pid=os.spawnlp(os.P_NOWAIT, "ariadne_worker.py", "ariadne_worker.py", "controller")
        local_worker_instance.port=42424
        local_worker_instance.hostname="127.0.0.1"
        loadconfig_local(ariadnetools.get_base_dir()+"/plugins")
    return local_worker_instance
