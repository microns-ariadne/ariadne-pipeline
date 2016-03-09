# sumtest_top.py -- Defines the top level to a very simple pipeline.
# The ultimate goal of the pipeline is to fetch a dataset and sum all of its elements.

import ariadneplugin
import h5py
import time

plugin_class = "sumtest_top"


class sumtest_top(ariadneplugin.Plugin):
    name="sumtest_top"
    internalsum=0
    datasetname=""
    checkval=0
    start_t=0
    end_t=0


    def run(self):
        self.start_t=time.time()
        handler=ariadneplugin.get_can_handle("dataset/hdf5")
        h=handler("testdataset.dataset")
        f=h.get_file("./data/", h.get_file_list("./data/")[0], "r")
        
        s=0
        for a in f['data']:
            s+=a

        print("Sum: "+str(s))
        f.close()
        self.internalsum=s

        f=h5py.File("./data/results.hdf5", "w")
        d=f.create_dataset("result", (1,))
        d[0]=s
        f.close()
        self.end_t=time.time()


    def depends(self):
        deplist=[]
        deplist.append(ariadneplugin.DependencyContainer("mkdir", {"dirname":"data"}))
        deplist.append(ariadneplugin.DependencyContainer("genericfetch", {"datasetname": self.datasetname, "dest": "./data/"}))
        return deplist


    def validate(self):
        try:
            f=h5py.File("./data/results.hdf5", "r")
            retval=(f['result'][0] == self.internalsum) and (self.internalsum == self.checkval)
            f.close()
            return retval
        except:
            print("Exception raised. Failing...")
            return 0


    def benchmark(self):
        return self.end_t-self.start_t


    def __init__(self, args={}, conffile="", conftoks=[]):
        if args=={}:
            return

        self.checkval=float(args['checkval'])
        self.datasetname=args['datasetname']
