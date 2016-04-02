from ariadne import plugin
import deftools
import os

plugin_class="rawdataset"


class rawdataset(plugin.DatasetPlugin):
    name = "rawdataset"
    data_list = []


    def can_handle(self, dataset_type):
        return dataset_type == "dataset/raw"


    def __init__(self, def_filename="", def_tokens=[]):
        if def_filename == "" and def_tokens == []:
            return
        
        tokens=[]
        if def_tokens==[]:
            tokens = deftools.parse_file(def_filename)
        else:
            tokens = def_tokens

        self.data_list = deftools.search(tokens, "urls")
