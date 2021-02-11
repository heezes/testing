# import test_logger
# import test_cases
import queue
import threading
import time
import test_mqtt
import test_response_interface
import test_cases

BLE_INTERFACE = 1
RTT_INTERFACE = 2

def main():
    '''
    Create two queue with and append them within an array
    Queue one is used to send realtime logs to mqtt server(Can be avoided by calling publish in ble callback)
    Queue two is used to parse and record the vehicle logs
    '''
    data_queue = []
    data_queue.append(queue.Queue())
    data_queue.append(queue.Queue())
    iot = test_mqtt.Mqtt(data_queue[0])
    interface = test_response_interface.interface(data_queue)
    test_case = test_cases.test_cases(data_queue[1], interface)
    x = threading.Thread(target=test_case.processResponse)
    x.start()
    while True:
        time.sleep(0.5)
        if(iot.test_request == 1):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
            iot.sendInfo(ret_info)
        elif (iot.test_request == 2):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
            iot.sendInfo(ret_info)
        elif (iot.test_request == 3):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
            iot.sendInfo(ret_info)

        elif (iot.test_request == 4):
            info = 'Executing Test Id: %d'%iot.test_request
            print(info)
            iot.sendInfo(info)
            iot.test_request = None
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
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
            ret_info = test_case.doLockUnlock(mode = 0,count = 1,\
                                        timeout = 20,wait_time = 5)
            iot.sendInfo(ret_info)

        # elif (iot.test_request == 7):
        # elif (iot.test_request == 8):
        # elif (iot.test_request == 9):

import log_one
import log_two

if __name__ == "__main__":
    one = log_one.my_log_one()
    two = log_two.my_log_two()
    one.print_info()
    two.print_info()
    # main()

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