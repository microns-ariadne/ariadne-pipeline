import logging
from cliff import command

class Command(command.Command):

    log = logging.getLogger(__name__)

    def run(self, parsed_args):
        self.log.debug('run(%s)', parsed_args)
        return super(Command, self).run(parsed_args)
