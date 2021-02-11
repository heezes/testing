import logging

class my_log_two():
    def __init__(self):
        self.log = logging.getLogger('test_two_logger')
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
    def print_info(self):
        self.log.debug("No No Bitches I'm here!")