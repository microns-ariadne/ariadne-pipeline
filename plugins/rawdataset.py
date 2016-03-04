import ariadneplugin
import deftools

plugin_class="rawdataset"


class rawdataset(ariadneplugin.DatasetPlugin):
    name="rawdataset"
    data_list=[]

    def can_handle(self, dataset_type):
        return dataset_type == "dataset/raw"


    def __init__(self, def_filename=""):
        if def_filename == "":
            return
        
        tokens=deftools.parse_file(def_filename)
        self.data_list=deftools.search(tokens, "urls")