from ariadne import static

class AriadneConfig(object):
    def __init__(self, config_file=None):
        self.cfg_file = config_file or static.ARIADNE_CFG_FILE
        self._config = None

    def __load_config(self):
        pass

    @property
    def config(self):
        if self._config is None:
            self._config = self.__load_config()
        return self._config