import logging

class my_log_one():
    def __init__(self):
        self.log = logging.getLogger('test_one_logger')
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
    def print_info(self):
        self.log.debug("Yo Yo Bitches I'm here!")