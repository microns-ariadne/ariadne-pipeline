# remote_executor.py -- Implementation of an ariadne_worker execution interface.
import ariadneplugin
import workerinterface
import time

plugin_class="remote_executor"


class remote_executor(ariadneplugin.ExecutorPlugin):
    name="remote_executor"


    def can_handle(self, ext):
        return ext=="exec/remote/parallel"


    def run(self, exec_list, do_validaion, do_benchmarking):
        start_t=time.time()
        inst=workerinterface.WorkerInstance()
        inst.hostname=exec_list[0].plugin_machine
        inst.port=exec_list[0].plugin_port
        
        for e in exec_list:
            workerinterface.run(inst, e.plugin_name, e.plugin_args)
        workerinterface.wait(inst)
        return 1, time.time()-start_t

    
