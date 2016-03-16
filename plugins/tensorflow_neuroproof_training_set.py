# tensorflow_neuroproof_training_set.py -- Plugin to set up a training dataset.
import os
import plugin

plugin_class="tensorflow_neuroproof_training_set"


class tensorflow_neuroproof_training_set(plugin.AriadneOp):
    name="tensorflow_neuroproof_training_set"


    def run(self, args):
        os.system("$PYTHON $ROOT/util/prepare_neuroproof_training.py -i Workspace/train_data.h5 -w Workspace/np_train_watersheds.h5 -p Workspace/np_train_probabilities.h5 -g Workspace/np_train_groundtruth.h5"


    def files_modified(self):
        flist=[]
        flist.append("Workspace/np_train_groundtruth.h5")
        return flist
