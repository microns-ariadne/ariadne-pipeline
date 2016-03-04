# ariadnetools.py -- Commonly used functions for ariadne.
import os
import sys

import ariadneplugin


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
        return os.environ['ARIADNE_BASE']
    except:
        print("WARNING: ARIADNE_BASE undefined.")
        return ""


def init_plugins():
    filename=get_base_dir()+"plugins/plugins.list"
    if file_exists(filename):
        ariadneplugin.load_plugins(filename, get_base_dir()+"plugins")
    else:
        print("WARNING: No plugins defined at "+filename)