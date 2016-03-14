# tensorflow_train.py -- Runs the training task for tensorflow.
import plugin
import os

plugin_class="tensorflow_train"


class tensorflow_train(plugin.AriadneOp):
    name="tensorflow_train"


    def run(self, args):
        os.system("mkdir -p Workspace/checkpoints")
        os.system("mkdir -p Workspace/summaries")
        os.system("$PYTHON $ROOT/membrane_classifier/train_resnet.py --learning_rate 0.01 --summary_dir Workspace/summaries --checkpoint_dir Workspace/checkpoints --hdf5 Workspace/train_data.h5 --batch_size 3 --num_modules $RESNET_COUNT --iterations 1000")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/checkpoints")
        flist.append("Workspace/summaries")
        return flist
