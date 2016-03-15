# tensorflow_neuroproof_classify.py -- Does neuroproof classification for test data.
import os
import plugin

plugin_class="tensorflow_neuroproof_classify"


class tensorflow_neuroproof_classify(plugin.AriadneOp):
    name="tensorflow_neuroproof_classify"


    def run(self, args):
        os.system("$PYTHON $ROOT/membrane_classifier/classify_resnet.py --num_modules $RESNET_COUNT --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/test_data.h5")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/test_data.h5")
        return flist
