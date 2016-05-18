import os
import luigi
import requests
import logging
from ariadne import static
from ariadne import utils
from ariadne import exceptions
from ariadne.common.command import Command

class StreamBaseTask(luigi.Task):
    dataset = luigi.Parameter()
    filename = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(os.path.join(static.ARIADNE_DATA_DIR,
                                              'raw_%s' % self.filename))


class StreamURLTask(StreamBaseTask):
    def run(self):
        req = requests.get(self.dataset, stream=True)
        if req.status_code == 200:
            with self.output().open('wb') as out_file:
                for chunk in req:
                    out_file.write(chunk)
        else:
            raise exceptions.UnknownDataset(self.dataset)


class StreamLocalTask(StreamBaseTask):
    def run(self):
        source = os.path.abspath(self.dataset)
        with self.output().open('wb') as out_file:
            with open(source, 'rb') as chunk:
                out_file.write(chunk.read())


class FetchTask(luigi.Task):
    dataset = luigi.Parameter()

    def run(self):
        if utils.is_url(self.dataset):
            filename = self.dataset.split('/')
            filename = filename[-1]
            yield StreamURLTask(dataset=self.dataset, filename=filename)
        else:
            filename = os.path.basename(self.dataset)
            yield StreamLocalTask(dataset=self.dataset, filename=filename)


class FetchCommand(Command):

    def get_parser(self, prog_name):
        parser = super(FetchCommand, self).get_parser(prog_name)
        parser.add_argument(
            "source",
            help="Source file"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.info('Starting Fetch')
        self.log.debug('Debug mode')
        print(parsed_args.source)
        output = luigi.build([FetchTask(dataset=parsed_args.source)],
                            local_scheduler=True)
        self.log.debug(output)
