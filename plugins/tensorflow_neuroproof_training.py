# tensorflow_neuroproof_training.py -- Performs training.
import os
import plugin

plugin_class="tensorflow_neuroproof_training"


class tensorflow_neuroproof_training(plugin.AriadneOp):
    name="tensorflow_neuroproof_training"


    def run(self, args):
        os.system("neuroproof_graph_learn Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/np_train_groundtruth.h5 --use_mito 0 --classifier-name Workspace/neuroproof_classifier.xml --num-iterations 1")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/neuroproof_classifier.xml")
        return flist
