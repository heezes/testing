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
import os
import sh


BLE_INTERFACE = 1
RTT_INTERFACE = 2

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    '''
    Create two queue with and append them within an array
    Queue one is used to send realtime logs to mqtt server(Can be avoided by calling publish in ble callback)
    Queue two is used to parse and record the vehicle logs
    '''
    time.sleep(1)
    parser = argparse.ArgumentParser(description='Target Device Name')
    parser.add_argument('--device_addr', action="store", dest='device_addr')
    parser.add_argument('--ble_interface', action="store", dest='ble_interface', type=str2bool)
    args = parser.parse_args()
    data_queue = []
    data_queue.append(queue.Queue())
    data_queue.append(queue.Queue())
    iot = test_mqtt.Mqtt(data_queue[0])
    interface = test_response_interface.interface(data_queue, args.device_addr, args.ble_interface)
    test_case = test_cases.test_cases(data_queue[1], interface)
    x = threading.Thread(target=test_case.processResponse)
    x.start()
    while True:
        time.sleep(0.5)
        #[mode, wait_time, count, timeout, ...]
        if iot.test_request == 6:
            print("Pushing data to git")
            git = sh.git.bake(_cwd='/home/pi/Desktop/testing')
            git.add("-A")
            if len(iot.test_commit_msg) > 1:
                git.commit(m=iot.test_commit_msg)
                iot.test_commit_msg = ""
            else:
                git.commit(m="Log file Syncing(Push made from testing/main.py)")
            git.push()
            os._exit(os.EX_OK)
        elif(iot.test_request == 1):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = 0
            if(iot.test_arg[0]>1):
                ret_info = test_case.doUnlock()
            else:
                ret_info = test_case.doUnlock(mode = iot.test_arg[0], wait_time = iot.test_arg[1])
            iot.sendInfo(ret_info)
        elif (iot.test_request == 2):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = 0
            if(iot.test_arg[0]>1):
                ret_info = test_case.doLock()
            else:
                ret_info = test_case.doLock(mode = iot.test_arg[0], wait_time = iot.test_arg[1])
            iot.sendInfo(ret_info)
        elif (iot.test_request == 7):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = 0
            if(iot.test_arg[0]>1):
                ret_info = test_case.doLockUnlock()
            else:
                ret_info = test_case.doLockUnlock(mode = iot.test_arg[0],count = iot.test_arg[2],\
                                            timeout = iot.test_arg[3],wait_time = iot.test_arg[1])
            iot.sendInfo(ret_info)
        elif (iot.test_request == 5):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = 0
 #           if(iot.test_arg[0]>1):
            ret_info = test_case.doSyncTrigger()
  #          else:
   #             ret_info = test_case.doSyncTrigger(wait_time = 15*60)
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

