import sys

from cliff.app import App
from ariadne.common.commandmanager import CommandManager


class AriadneCLI(App):
    def __init__(self):
        super(AriadneCLI, self).__init__(
            description='Run, and manage machine learning pipelines.',
            version='0.1',
            command_manager=CommandManager('ariadne.clisub.base'),
            deferred_help=True
        )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_ariadne')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    cli = AriadneCLI()
    return cli.run(argv)
