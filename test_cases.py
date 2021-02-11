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
        self.log = logging.getLogger('test_cases')
        self.log.setLevel(logging.DEBUG)
        # create a file e
        handler = logging.FileHandler('hello.log')
        handler.setLevel(logging.DEBUG)

        # # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the file handler to the logger
        self.log.addHandler(handler)

    def processResponse(self):
        while True:
            self.parser.log_and_parse(self.queue)
            time.sleep(0.05)
#wait_time: Time to wait for response
#mode: Key or Keyless
#timeout: Wait time bw two operation
    def doLock(self, mode, wait_time):
        results = True
        if(mode):
            global gpio_pins
            self.hardware.enable_gpio(gpio_pins[0])
            if(self.parser.getLockResult(wait_time) == False):
                self.log.warning('Lock Failed') #Lock Failed
                results =  False
        else:
            self.ble.sendCommand(0x06)
            if(self.parser.getLockResult(wait_time) == False):
                self.log.warning('Lock Failed') #Lock Failed
                results = False
        results_info = "Lock Test Results - Passed: %s "%(str(results))
        self.log.debug(results_info)
        return results_info

    def doUnlock(self, mode, wait_time):
        results = True
        if(mode):
            global gpio_pins
            self.hardware.disable_gpio(gpio_pins[0])
            if(self.parser.getUnlockResult(wait_time) == False):
                self.log.warning('Unlock Failed') #Unlock Failed
                results = False
        else:
            self.ble.sendCommand(0x09)
            if(self.parser.getUnlockResult(wait_time) == False):
                self.log.warning('Unlock Failed') #Unlock Failed
                results = False
        results_info = "Unlock Test Results - Passed: %s "%(str(results))
        self.log.debug(results_info)
        return results_info

    def doSyncTrigger(self, wait_time):
        results = True
        self.ble.sendCommand(0x08)
        if(self.parser.getUnlockResult(wait_time) == False):
            self.log.warning('Sync Failed') #Unlock Failed
            results = False
        results_info = "Sync Test Results - Passed: %s "%(str(results))
        self.log.debug(results_info)
        return results_info

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
                if(self.parser.getLockResult(wait_time) == False):
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
                if(self.parser.getLockResult(wait_time) == False):
                    self.log.warning('Lock Failed') #Lock Failed
                    results.append(False)
                    break
            results.append(True)
        passed_test = 0
        for i in range(len(results)):
            if(results[i]):
                passed_test =+ 1
        results_info = "Lock/Unlock Test Results(%d/%d) - Passed: %d Failed: %d"%(count, len(results), passed_test, \
                        len(results)-passed_test)
        self.log.debug(results_info)
        return results_info
