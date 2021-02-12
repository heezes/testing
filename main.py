import queue
import threading
import time
import test_mqtt
import test_response_interface
import test_cases
import logging
from logging.handlers import RotatingFileHandler
import sys
import argparse

BLE_INTERFACE = 1
RTT_INTERFACE = 2

def logRttData(queue):
    logger = logging.getLogger('main.py')
    logger.setLevel(logging.DEBUG)
    # create a file e
    handler = RotatingFileHandler('rtt.log', maxBytes=5*1024, backupCount=1)
    handler.setLevel(logging.DEBUG)

    # # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the file handler to the logger
    logger.addHandler(handler)
    while True:
        time.sleep(0.01)
        if(queue.empty() == False):
            data = queue.get()
            logger.debug(str(data[0]))


def main():
    '''
    Create two queue with and append them within an array
    Queue one is used to send realtime logs to mqtt server(Can be avoided by calling publish in ble callback)
    Queue two is used to parse and record the vehicle logs
    '''
    parser = argparse.ArgumentParser(description='Target Device Name')
    parser.add_argument('--device_addr', action="store", dest='device_addr')
    args = parser.parse_args()
    data_queue = []
    data_queue.append(queue.Queue())
    data_queue.append(queue.Queue())
    iot = test_mqtt.Mqtt(data_queue[0])
    interface = test_response_interface.interface(data_queue, args.device_addr)
    test_case = test_cases.test_cases(data_queue[1], interface)
    x = threading.Thread(target=test_case.processResponse)
    y = threading.Thread(target=logRttData, args=(data_queue[0],))
    x.start()
    y.start()
    while True:
        time.sleep(0.5)
        if iot.test_request == 0:
            #push data to git and exit program
            os.exit(0)
        elif(iot.test_request == 1):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doUnlock(mode = 0, wait_time = 10)
            iot.sendInfo(ret_info)
        elif (iot.test_request == 2):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLock(mode = 0, wait_time = 10)
            iot.sendInfo(ret_info)
        elif (iot.test_request == 5):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
            iot.sendInfo(ret_info)
        elif (iot.test_request == 6):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doSyncTrigger(wait_time = 15*60)
            iot.sendInfo(ret_info)

if __name__ == "__main__":
    main()

'''
Hardware Env: Raspberry Pi

Software Env: Python 3.9

Planned the software architecture

Base layer components

VIM interface: For debug/result logs

openOCD

Ble

GPIO interface: For generating events

Top layer components

Result parsing class: This class is used to extract logs from vim interface. The result is passed on as it is or parsed depending upon requirement

Test cases class: This class is used to generate events and check if the event succeeded or not.

CloudMqtt Class:  This class conencts the host to cloud for remote operation of test cases and debug log access

Main Application: Yet to decide


'''