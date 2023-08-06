from .step import Step
import logging


class Preflight(Step):
    def process(self, data, inputs, utils):
        logging.info('in Preflight')
        utils.create_dirs()
