# hdf5dataset.py -- A dummy HDF5 dataset handler.
import tools
import deftools
import plugin
import os

plugin_class="hdf5dataset"


class hdf5dataset(plugin.DatasetPlugin):
    name="hdf5dataset"
    data_list=[]


    def can_handle(self, dataset_type):
        return dataset_type=="dataset/hdf5"


    def __init__(self, def_filename="", def_tokens=[]):
        if def_filename=="" and def_tokens==[]:
            return

        tokens=[]
        if def_tokens==[]:
            tokens=deftools.parse_file(def_filename)
        else:
            tokens=def_tokens

        self.data_list=deftools.search(tokens, "urls")
