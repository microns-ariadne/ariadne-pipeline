# ariadnetools.py -- Commonly used functions for ariadne.
import os
import sys

import plugin


def get_extension(name):
    tmp=name.split('.')

    ext=""
    
    for s in tmp[1:]:
        ext += "."+s

    return ext


def get_url_filename(url):
    tmp=url.split('/')
    
    if len(tmp)>0:
        return tmp[len(tmp)-1]
    else:
        return ""


def get_url_extension(url):
    return get_extension(get_url_filename)


def file_exists(filename, extensions=[]):
    if extensions==[]:
        return os.path.isfile(filename)

    cur_status=0

    for e in extensions:
        cur_status=curStatus or file_exists(filename+e)

    return cur_status


def get_file_exists(filename, extensions):
    if file_exists(filename):
        return filename

    for e in extensions:
        if file_exists(filename+e):
            return filename+e

    return ""


def get_base_dir():
    try:
        d=os.environ['ARIADNE_BASE']
        if d[len(d)-1] != '/':
            d+='/'
        return d
    except:
        # This may be significantly better than using the environment variable.
        genpath=os.path.realpath(sys.path[0]+"/..")
        return genpath


def init_plugins(bdir=""):
    filename=""
    if bdir=="":
        filename=get_base_dir()+"/plugins/plugins.list"
    else:
        sys.path.append(bdir)
        filename=bdir+"/plugins.list"

    if file_exists(filename):
        plugin.load_plugins(filename, get_base_dir()+"/plugins")
    else:
        print("WARNING: No plugins defined at "+filename)


def getenv(var_name):
    try:
        print(os.environ[var_name])
        return os.environ[var_name]
    except:
        return ""


def setenv(var_name, value):
    os.environ[var_name]=value
