# serial_executor.py -- Defines a basic serial execution plugin.
import ariadneplugin
import time

plugin_class = "serial_executor"


class serial_executor(ariadneplugin.ExecutorPlugin):
    name="serial_executor"

    def can_handle(self, extension):
        return extension="exec/local/serial"


    def run(self, exec_list, do_validation, do_benchmarking):
        start_t=time.time()
        retv=1
        for e in exec_list:
            pclass=ariadneplugin.search_plugin(e.plugin_name)
            if pclass==None:
                print("ERROR: Plugin not present: "+e.plugin_name)
                raise Exception
            pl=pclass(e.plugin_args)
            pl.run()
            if do_validation:
                if pl.validate():
                    print("PASS: "+pl.name)
                else:
                    print("FAIL: "+pl.name)
                    retv=0
        return retv, time.time-start_t

            
                
