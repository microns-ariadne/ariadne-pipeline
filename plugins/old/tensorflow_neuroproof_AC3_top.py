# tensorflow_neuroproof_AC3_top -- Top plugin for the tensorflow-neuroproof-AC3 pipeline.
# This plugin was implemented in a fairly lazy way, ie. all of
# the stages in the pipeline are pretty much just handled here. 
# Ideally, each stage in the pipeline would be its own plugin.

import ariadneplugin
import ariadnetools
import os
import sys

plugin_class="tensorflow_neuroproof_AC3_top"


class tensorflow_neuroproof_AC3_top(ariadneplugin.Plugin):
    name="tensorflow_neuroproof_AC3_top"
    base_dir=""


    def run(self):
        print("importing images and ground truth.")
        os.system("python $ROOT/util/create_input_datasets.py -i Data/ac3train/input -l Data/ac3train/labels -o workspace/train_data.h5")
        print("creating membrane training set")
        os.system("python $ROOT/util/create_membrane_training.py -i workspace/train_data.h5 -p 5 -n 10")

        print("running training")
        os.system("python $ROOT/membrane_classifier/train_resnet.py --learning_rate 0.01 --summary_dir Workspace/summaries --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/train_data.h5 --batch_size 3 --num_modules $RESNET_COUNT --iterations 1000")
        
        print("classifying images in training set")
        os.system("python $ROOT/membrane_classifier/classify_resnet.py --num_modules $RESNET_COUNT --checkpoint_dir Workspace/checkpoints --hdf5 workspace/train_data.h5")
        
        print("creating watershed in training set")
        os.system("python $ROOT/util/create_watersheds.py -i workspace/train_data.h5 -s 250")

        print("setting up Neuroproof training set")
        os.system("python $ROOT/util/prepare_neuroproof_training.py -i Workspace/train_data.h5 -w Workspace/np_train_watersheds.h5 -p Workspace/np_train_probabilities.h5 -g Workspace/np_train_groundtruth.h5")

        print("training neuroproof")
        os.system("neuroproof_graph_learn Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/np_train_groundtruth.h5 --use_mito 0 --classifier-name Workspace/neuroproof_classifier.xml")

        print("running neuroproof on training data")
        os.system("neuroproof_graph_predict Workspace/np_train_watersheds.h5 Workspace/np_train_probabilities.h5 Workspace/neuroproof_classifier.xml --output-file Workspace/np_train_merged.h5")

        print("importing testing images and ground truth.")
        os.system("python $ROOT/util/create_input_datasets.py -i Data/ac3test/input -l Data/ac3test/labels -o Workspace/test_data.h5")

        print("classifying images in training set")
        os.system("python $ROOT/membrane_classifier/classify_resnet.py --num_modules $RESNET_COUNT --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/test_data.h5")

        print("creating watershed in testing set")
        os.system("python $ROOT/util/create_watersheds.py -i Workspace/test_data.h5 -s 250")

        print("setting up Neuroproof testing set")
        os.system("$ROOT/util/prepare_neuroproof_training.py -i Workspace/test_data.h5 -w Workspace/np_test_watersheds.h5 -p Workspace/np_test_probabilities.h5 -g Workspace/np_test_groundtruth.h5")

        print("running neuroproof on testing data")
        os.system("neuroproof_graph_predict Workspace/np_test_watersheds.h5 Workspace/np_test_probabilities.h5 Workspace/neuroproof_classifier.xml --output-file Workspace/np_test_merged.h5")


    def depends(self):
        deplist=[]
        wsdir=self.base_dir+"/workspace"
        deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': wsdir}))
        dir1=wsdir+"/checkpoints"
        dir2=wsdir+"/summaries"
        deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': dir1}))
        deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': dir2}))

#        deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': (self.base_dir+"/Workspace")})
        #deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': self.base_dir+"/Workspace/checkpoints"})
        #deplist.append(ariadneplugin.DependencyContainer("mkdir", {'dirname': self.base_dir+"/Workspace/summaries"})
        return deplist


    def validate(self):
        return 1

    def check_inputs(self):
        return 1

    def benchmark(self):
        return 0

    def success(self):
        return 1

    def __init__(self, args={}, conffile="", conftoks=[]):
        #if args=={}:
        #    return
        if ariadnetools.getenv("ROOT")=="":
            return
        self.base_dir=ariadnetools.getenv("ROOT")
        self.resnet_count=int(ariadnetools.getenv("RESNET_COUNT"))
        print("$RESNET_COUNT="+ariadnetools.getenv("RESNET_COUNT"))
