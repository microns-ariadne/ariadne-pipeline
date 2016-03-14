# Creates training datasets for the tensorflow task.
import os
import pipeline

plugin_class="tensorflow_create_training"


class tensorflow_create_training(plugin.AriadneOp):
    name="tensorflow_create_training"


    def run(self, args):
        os.system("$PYTHON $ROOT/util/create_membrane_training.py -i Workspace/train_data.h5 -p 5 -n 10")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/train_data.h5")
        return flist
