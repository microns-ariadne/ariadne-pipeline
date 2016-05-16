# tensorflow_classify.py -- Does classification for tensorflow.
import plugin
import os

plugin_class="tensorflow_classify"


class tensorflow_classify(plugin.AriadneOp):
    name="tensorflow_classify"


    def run(self, args):
        os.system("$PYTHON $ROOT/membrane_classifier/classify_resnet.py --num_modules $RESNET_COUNT --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/train_data.h5")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/")
        return flist()

