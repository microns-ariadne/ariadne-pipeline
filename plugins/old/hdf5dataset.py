# hdf5dataset.py -- A dataset plugin to handle hdf5 datasets.

import ariadneplugin
import ariadnetools
import deftools
import h5py
import os

plugin_class = "hdf5dataset"


class hdf5dataset(ariadneplugin.DatasetPlugin):
    name="hdf5dataset"
    data_list=[]

    def can_handle(self, dataset_type):
        return dataset_type == "dataset/hdf5" or dataset_type == "dataset/hdf"


    def get_file_list(self, destination):
        dir_listing=os.listdir(destination)
        file_list=[]
        for entry in dir_listing:
            if ariadnetools.get_extension(entry) == ".hdf5":
                file_list.append(entry)
        return file_list


    def get_file(self, destination, name, mode):
        if destination=="":
            destination="."
        if len(mode) != 1:
            print("WARNING: Invalid HDF5 file mode: "+mode)

        return h5py.File(destination+"/"+name, mode)


    def __init__(self, def_filename="", def_toks=[]):
        if def_filename=="" and def_toks==[]:
            return

        tokens=[]
        if def_toks==[]:
            tokens=deftools.parse_file(def_filename)
        else:
            tokens=def_toks

        self.data_list=deftools.search(tokens, "urls")
