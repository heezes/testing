import logging
from logging.handlers import RotatingFileHandler
import parser_util
import test_hardware_interface
import time

gpio_pins   = [6,13,26] #[key, wheel, access screw]
KEY_PIN     = 0
WHEEL_PIN   = 1
SCREW_PIN   = 2

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
        handler = RotatingFileHandler('report.log', maxBytes=5*1024*1024, backupCount=1)
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

    """
    @brief: This function should be called to perform a lock activity and checks if it succeded
    @param: mode: 0:Key based access, 1: Keyless access
    @param: wait_time: Time to wait for the response (seconds)
    """
    def doLock(self, mode = 0, wait_time = 10):
        results = True
        if(mode):
            global gpio_pins
            self.hardware.disable_gpio(KEY_PIN)
            if(self.parser.getLockResult(wait_time) == False):
                self.log.debug('Lock Failed') #Lock Failed
                results =  False
        else:
            self.ble.sendCommand(0x06)
            if(self.parser.getLockResult(wait_time) == False):
                self.log.debug('Lock Failed') #Lock Failed
                results = False
        results_info = "Lock Test Results - Passed: %s "%(str(results))
        self.log.debug(results_info)
        return results_info

    """
    @brief: This function should be called to perform a unlock activity and checks if it succeded
    @param: mode: 0:Key based access, 1: Keyless access
    @param: wait_time: Time to wait for the response (seconds)
    """
    def doUnlock(self, mode = 0, wait_time = 10):
        results = True
        if(mode):
            global gpio_pins
            self.hardware.enable_gpio(KEY_PIN)
            if(self.parser.getUnlockResult(wait_time) == False):
                self.log.debug('Unlock Failed') #Unlock Failed
                results = False
        else:
            self.ble.sendCommand(0x09)
            if(self.parser.getUnlockResult(wait_time) == False):
                self.log.debug('Unlock Failed') #Unlock Failed
                results = False
        results_info = "Unlock Test Results - Passed: %s "%(str(results))
        self.log.debug(results_info)
        return results_info

    """
    @brief: This function should be called to perform a sync activity and checks if it succeded
    @param: wait_time: Time to wait for the response (seconds)
    """
    def doSyncTrigger(self, wait_time = 15*60):
        # results = True
        self.ble.sendCommand(0x08)
        # if(self.parser.getSyncResult(wait_time) == False):
        #     self.log.debug('Sync Failed') #Unlock Failed
        #     results = False
        # results_info = "Sync Test Results - Passed: %s "%(str(results))
        results_info = "Sync Triggered"
        self.log.debug(results_info)
        return results_info

    """
    @brief: This function should be called to perform a lock/unlock activity in loop and checks if it succeded
    @param: mode: 0:Key based access, 1: Keyless access
    @param: count: No of time lock/unlock combination is repeated
    @param: timeout: Time to wait between each lock/unlock
    @param: wait_time: Time to wait for the response (seconds)
    """
    def doLockUnlock(self, mode = 0, count = 10, timeout = 2, wait_time = 10):
        self.log.debug('Performing Lock/Unlock rest %d times', count)
        results = []
        for i in range(count):
            time.sleep(float(timeout))
            if(mode):
                global gpio_pins
                self.hardware.enable_gpio(KEY_PIN)
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.debug('Unlock Failed') #Unlock Failed
                    results.append(False)
                    break
                time.sleep(timeout)
                self.hardware.disable_gpio(KEY_PIN)
                if(self.parser.getLockResult(wait_time) == False):
                    self.log.debug('Lock Failed') #Lock Failed
                    results.append(False)
                    break
            else:
                self.ble.sendCommand(0x09)
                if(self.parser.getUnlockResult(wait_time) == False):
                    self.log.debug('Unlock Failed') #Unlock Failed
                    results.append(False)
                    break
                time.sleep(timeout)
                self.ble.sendCommand(0x06)
                if(self.parser.getLockResult(wait_time) == False):
                    self.log.debug('Lock Failed') #Lock Failed
                    results.append(False)
                    break
            results.append(True)
        passed_test = 0
        print(results)
        for i in range(len(results)):
            if(results[i]):
                passed_test = passed_test + 1
        results_info = "Lock/Unlock Test Results(%d/%d) - Passed: %d Failed: %d"%(count, len(results), passed_test, \
                        len(results)-passed_test)
        self.log.debug(results_info)
        return results_info
