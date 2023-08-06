from .step import Step
import logging


class Postflight(Step):
    def process(self, data, inputs, utils):
        logging.info('in Postflight')

