import logging
import parser_util
import test_hardware_interface
import time

gpio_pins = [1,2,3,4]

class test_cases():
    def __init__(self, queue, ble):
        self.casesPassed = 0
        self.ble = ble
        self.queue = queue
        self.parser = parser_util.response_parser()
        self.hardware = test_hardware_interface.hardware(gpio_pins)
        logger = logging.getLogger('test_cases')
        self.log = logger.setLevel(logging.INFO)
        # create a file handler
        handler = logging.FileHandler('hello.log')
        handler.setLevel(logging.INFO)

        # # create a logging format
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # # add the file handler to the logger
        # self.log.addHandler(handler)


        # logging.basicConfig(filename = 'debug.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
        # self.log = logging.getLogger('test_cases')
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=self.log.DEBUG)

    def processResponse(self):
        while True:
            self.parser.log_and_parse(self.queue)
            time.sleep(0.1)

    def doLockUnlock(self, mode, count, timeout, wait_time):
        self.log.debug('Performing Lock/Unlock rest %d times', count)
        results = []
        for i in range(count):
            if(mode):
                global gpio_pins
                self.hardware.toggle_gpio(gpio_pins[0])
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.warning('Unlock Failed') #Unlock Failed
                    results.append(False)
                    break
                time.sleep(timeout)
                self.hardware.toggle_gpio(gpio_pins[0])
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.warning('Lock Failed') #Lock Failed
                    results.append(False)
                    break
            else:
                self.ble.sendCommand(0x09)
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.warning('Unlock Failed') #Unlock Failed
                    results.append(False)
                    break
                time.sleep(timeout)
                self.ble.sendCommand(0x06)
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.warning('Lock Failed') #Lock Failed
                    results.append(False)
                    break
            results.append(True)
        passed_test = 0
        for i in range(len(results)):
            if(results[i]):
                passed_test =+ 1
        results_info = "Test Results(%d/%d) - Passed: %d Failed: %d"%(count, len(results), passed_test, \
                        len(results)-passed_test)
        self.log.debug(results_info)
        return results_info
