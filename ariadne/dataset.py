# dataset.py -- Tools for plugins that require dataset integration.
import os
import tools
import plugin
import deftools



def fetchunpack_dataset(dataset_name, dataset_destination=""):
    if dataset_destination=="":
        dataset_destination=tools.get_default_dataset_dir()+"/"+dataset_name
        try:
            os.mkdir(dataset_destination)
        except:
            # Check if there's a more serious error:
            if not os.path.isdir(dataset_destination):
                raise OSError

    # Determine where, exactly, this dataset is:
    fullpath="%s/%s.dataset" % (tools.get_default_dataset_dir(), dataset_name)
    if not tools.file_exists(fullpath):
        fullpath="./%s.dataset" % dataset_name

    dataset_filename=fullpath

    if not tools.file_exists(fullpath):
        print("ERROR: Dataset "+dataset_name+" does not exist either in ./ or %s." 
                % tools.get_default_dataset_dir())
        return None
    dataset_contents = deftools.parse_file(dataset_filename)
    dataset_type = deftools.search(dataset_contents, "type")[0]
    if len(dataset_type) == 0:
        print("ERROR: Dataset has unspecified type. Cannot handle.")
        exit(2)

    dataset_handler=plugin.get_can_handle(dataset_type)

    if dataset_handler==None:
        print("Could not find a plugin to handle dataset type: %s" % dataset_type)
        return None

    h=dataset_handler(dataset_filename)

    pre=os.listdir(dataset_destination)
    h.fetch(dataset_destination)    
    h.unpack(dataset_destination)
    post=os.listdir(dataset_destination)

    deltas=tools.get_dir_delta(pre, post)

    f=open("%s/%s.log" % (dataset_destination, dataset_name), "w")

    for d in deltas:
        f.write("%d %s\n" % (d[0], d[1]))

    f.close()

    return dataset_destination

    
def check_datset_fetched(datasetname, dest=""):
    if dest=="":
        dest=tools.get_default_dataset_dir()+"/"+dataset_name
        if not os.path.isdir(dest):
            return 0

    return tools.file_exists("%s/%s.log" % (dest, datasetname))


def get_dataset_files(dataset_name, dataset_dir):
    """Gets a listing of all of the files in a dataset.
       Assumes that the dataset exists and has been fetched."""

    if not tools.file_exists(dataset_dir+"/%s.log" % dataset_name):
        print("ERROR: Dataset transaction log does not exist. Returning directory listing...")
        return os.listdir(dataset_dir)

    f=open(dataset_dir+"/%s.log" % dataset_name, "r")
    contents=f.read()
    f.close()
    
    lines=contents.splitlines()
    flist=[]

    for l in lines:
        toks=lines.split()

        try:
            flist.append(toks[1])
        except:
            pass

    return flist


def get_dataset_plugin(datasetname):
    fullpath="./%s.dataset" % datasetname

    if not tools.file_exists(fullpath):
        fullpath="%s/%s.dataset" % (tools.get_default_dataest_dir(), datasetname)

    if not tools.file_exists(fullpath):
        print("ERROR: Dataset definition file for %s not found." % datasetname)
        return None

    toks=deftools.parse_file(fullpath)

    typetok=deftools.search(toks, "type")[0]

    return plugin.get_can_handle(typetok)
