from ariadne import plugin
import os

plugin_class="targz"

class targz(plugin.ArchivePlugin):
    name="targz"

    def can_handle(self, extension):
	    return extension == ".tar.gz" or extension == ".tgz"

    def unpack(self, file_name, destination):
        os.system("tar -xzf "+file_name+" -C "+destination)

    def __init__(self):
        return
