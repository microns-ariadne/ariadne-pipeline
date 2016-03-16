# tensorflow_create_dataset.py -- Creates input datasets for the tensorflow task.
import plugin
import os

plugin_class="tensorflow_create_dataset"


class tensorflow_create_dataset(plugin.AriadneOp):
    name="tensorflow_create_dataset"


    def run(self, args):
        os.system("$PYTHON $ROOT/util/create_input_datasets.py -i Data/ac3train/input -l Data/ac3train/labels -o Workspace/train_data.h5")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/train_data.h5")
        return flist
