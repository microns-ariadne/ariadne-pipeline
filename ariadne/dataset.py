# dataset.py -- Tools for plugins that require dataset integration.
import tools
import plugin
import deftools


loglist=[]


def fetchunpack_datset(dataset_name, dataset_destination=""):
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
        return
    dataset_contents = deftools.parse_file(dataset_filename)
    dataset_type = deftools.search(dataset_contents, "type")[0]
    if len(dataset_type) == 0:
        print("ERROR: Dataset has unspecified type. Cannot handle.")
        exit(2)

    dataset_handler=plugin.get_can_handle(dataset_type)

    if dataset_handler==None:
        print("Could not find a plugin to handle dataset type: %s" % dataset_type)
        return

    h=dataset_handler(dataset_filename)

    pre=os.listdir(dataset_destination)
    h.fetch(dataset_destination)    
    h.unpack(dataset_destination)
    post=os.listdir(dataset_destination)

    deltas=tools.get_dir_delta(pre, post)

    f=open("%s/%s.log" % (dataset_destination, datasetname))

    for d in deltas:
        f.write("%d %s\n" % (d[0], d[1]))

    f.close()

    
def check_datset_fetched(datasetname, dest=""):
    if dest=="":
        dest=tools.get_default_dataset_dir()+"/"+dataset_name
        if not os.path.isdir(dest):
            return 0

    return tools.file_exists("%s/%s.log" % (dest, datasetname))


def get_dataset_files(datasetname):
    pass

