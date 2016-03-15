# tensorflow_import_imggt -- Imports images and groundtruth
import os
import plugin

plugin_class="tensorflow_import_imggt"


class tensorflow_import_imggt(plugin.AriadneOp):
    name="tensorflow_import_imggt"


    def run(self, args):
        os.system("$PYTHON $ROOT/util/create_input_datasets.py -i Data/ac3test/input -l Data/ac3test/labels -o Workspace/test_data.h5")


    def files_modified(self):
        flist=[]
        flist.append("Workspace/test_data.h5")
        return flist
