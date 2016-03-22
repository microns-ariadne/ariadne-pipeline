# ariadnetools.py -- Commonly used functions for ariadne.
import os
import sys
import deftools
import plugin


def get_extension(name):
    """Returns the full extension for a given file.
       Example: 'mytar.tar.gz' -> '.tar.gz'
    """
    tmp=name.split('.')

    ext=""
    
    for s in tmp[1:]:
        ext += "."+s

    return ext


def get_url_filename(url):
    """Attempts to get the remote filename referred to by the url specified."""
    tmp=url.split('/')
    
    if len(tmp)>0:
        return tmp[len(tmp)-1]
    else:
        return ""


def get_url_extension(url):
    """Returns the extension of the given url."""
    return get_extension(get_url_filename)


def file_exists(filename, extensions=[]):
    """Returns 1 if the specified file exists. Can also
       apply a list of extensions to the file while searching.
    """
    if extensions==[]:
        return os.path.isfile(filename)

    cur_status=0

    for e in extensions:
        cur_status=curStatus or file_exists(filename+e)

    return cur_status


def get_file_exists(filename, extensions):
    """Returns the first filename with any of the extensions 
       in the list if it exists.
    """
    if file_exists(filename):
        return filename

    for e in extensions:
        if file_exists(filename+e):
            return filename+e

    return ""


def get_base_dir():
    """Attempts to locate ariadne's install directory."""
    try:
        d=os.environ['ARIADNE_BASE']
        if d[len(d)-1] != '/':
            d+='/'
        return d
    except:
        # This may be significantly better than using the environment variable.
        genpath=os.path.realpath(sys.path[0]+"/..")
        return genpath


def get_default_dataset_dir():
    """Returns the default directory in which to search for dataset files."""
    return get_base_dir()+"/examples"


def get_default_config_file():
    """Returns the default configuration file location."""
    return os.path.expanduser('~')+"/.ariadnerc"


def get_default_conf_toks():
    """Returns a list of default options for a configuration file."""
    usrbase=os.path.expanduser('~')
    conf_toks=[]
    conf_toks.append(["basedir", usrbase+"/ariadne"])
    conf_toks.append(["tmpdir", usrbase+"/ariadne/tmp"])
    conf_toks.append(["datadir", usrbase+"/ariadne/data"])
    conf_toks.append(["plugindirs"])
    return conf_toks


def prep_default_config_file(conffile):
    """Creates an ariadne directory structure and writes a default configuration file."""
    usrbase=os.path.expanduser('~')
    try:
        os.mkdir(usrbase+'/ariadne')
        os.mkdir(usrbase+'/ariadne/tmp')
        os.mkdir(usrbase+'/ariadne/data')
    except OSError: # Then the files likely exist.
        pass
    deftools.write_file(get_default_conf_toks(), conffile)


def init_plugins(bdir=""):
    """Loads and initializes all plugins in the specified directory or the default directory
       if unspecified.
    """
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
    """Attempts to return the specified environment variable."""
    try:
        print(os.environ[var_name])
        return os.environ[var_name]
    except:
        return ""


def setenv(var_name, value):
    """Attempts to set the specified environment variable."""
    os.environ[var_name]=value


def get_dir_delta(beforelisting, afterlisting):
    """Determines which files were added, removed, or remained the same in a directory."""
    deltas=[]

    # Find files added.
    for a in afterlisting:
        added=1

        for b in beforelisting:
            added=added and b!=a

        deltas.append((added, a))

    # Find the files removed (if any):
    for b in beforelisting:
        removed=1

        for a in afterlisting:
            removed=removed and b!=a

        if removed:
            deltas.append((-1, b))

    return deltas
