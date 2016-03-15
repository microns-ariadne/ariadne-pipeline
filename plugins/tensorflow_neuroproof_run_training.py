# tensorflow_neuroproof_run_training.py -- Runs neuroproof on the training data.
import os
import plugin

plugin_class="tensorflow_neuroproof_run_training.py"


class tensorflow_neuroproof_run_training(plugin.AriadneOp):
    name="tensorflow_neuroproof_run_training"


    def run(self, args):
        os.system("neuroproof_graph_predict Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/neuroproof_classifier.xml --output-file Workspace/np_train_merged.h5")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/np_train_merged.h5")
        return flist
