import pygatt
import time
from binascii import hexlify
import sys
import json
import logging
import socket
import threading
from logging.handlers import RotatingFileHandler

class interface():
    def __init__(self, data_queue, device_addr, ble_interface=True):
        #intialize the vim response mechanism
        self.device = 0
        self.socket = 0
        self.data_queue = []
        self.device_addr = device_addr
        self.data_queue.append(data_queue[0])
        self.data_queue.append(data_queue[1])
        self.ble_interface = interface #Use BLE interface
        self.opcode_response = None #BLE opcode response for a command
        self.logger = logging.getLogger('test_response_interface.py')
        self.logger.setLevel(logging.DEBUG)
        # create a file e
        handler = RotatingFileHandler('rtt.log', maxBytes=5*1024*1024, backupCount=1)
        handler.setLevel(logging.DEBUG)

        # # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the file handler to the logger
        self.logger.addHandler(handler)
        self.connectToInterface(interface)



    """
    @brief: Callback function for charateristic notification
    @param: handle: characteristic handle
    @param: value: encoded data
    """
    def data_handler_cb(self, handle, value):
        try:
            self.opcode_response = value.decode("utf-8")
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    """
    @brief: Callback function for charateristic notification
    @param: handle: characteristic handle
    @param: value: encoded data
    """
    def received_data_cb(self, handle, value):
        if(self.ble_interface):
            try:
                data = value.decode("utf-8")
                # self.data_queue[0].put((data,))
                self.data_queue[1].put((data,))
                self.logger.debug(data)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    """
    @brief: Callback function for disconnection notification
    """
    def Disconnected(self, event):
        print ("disconnected from BLE")

    """
    @brief: This function initializes the response interface
    @param: interface: Response interface(For now only ble is supported. Rtt physical via openocd could be an option)
    """
    def connectToInterface(self, interface):
        adapter = pygatt.GATTToolBackend(search_window_size=200)
        adapter.start()
        device_info = adapter.filtered_scan(self.device_addr, timeout=1)
        dev_info = device_info[0]
        print("Connecting to device %s:%s"%(self.device_addr, dev_info['address']))
        if(device_info):
            self.device = adapter.connect(dev_info['address'], address_type = pygatt.BLEAddressType.random, auto_reconnect=True)
            self.device.register_disconnect_callback(self.Disconnected)
            self.device.exchange_mtu(128)
            self.device.subscribe("ed0ef62e-9b0d-11e4-89d3-123b93f75eba",\
                            callback=self.data_handler_cb,\
                            indication=False)
            self.device.char_write("ed0ef62e-9b0d-11e4-89d3-123b93f75dba", bytearray([0x01]), True)
            print("Auth Command Written")
            token = b'\x1d\x49\x00\x00'
            self.device.char_write("ed0ef62e-9b0d-11e4-89d3-123b93f75fba", token, True)
            print("Authenticated")
            # while self.opcode_response != 0x01:
            #     pass
            self.device.char_write("ed0ef62e-9b0d-11e4-89d3-123b93f75dba", bytearray([0x0C]), True)
            print("Enabling Debug")
            if self.ble_interface == True:
                self.device.subscribe("ed0ef62e-9b0d-11e4-89d3-123b93f75fba",\
                                callback=self.received_data_cb,\
                                indication=False)
            else:
                self.connectToRttServer()
                rttThread = threading.Thread(target=self.retrieveRttData)
                rttThread.start()
        # self.connectToRttServer()
        # rttThread = threading.Thread(target=self.retrieveRttData)
        # rttThread.start()


    """
    @brief: This function can request the target to perform an activity depending upon the command
    @param: command: Ble command to perform a certain activity
    """
    def sendCommand(self, command):
        if(self.device._connected):
            self.opcode_response = None
            self.device.char_write("ed0ef62e-9b0d-11e4-89d3-123b93f75dba", bytearray([command]), True)
            # while self.opcode_response == None:
            #     time.sleep(0.5)
            #     pass
            # print("Response %s"%self.opcode_response)
            # return self.opcode_response
            return True
        else:
            print("BLE not connected")
            return False

    """
    @brief: This function creates a localhost connection to rtt server hosted by openocd
    """
    def connectToRttServer(self):
        port = 9090 # socket server port number
        host = "127.0.0.1"
        self.socket = socket.socket()  # instantiate
        self.socket.connect((host, port))  # connect to the server

    """
    @brief: This function retrieves data from the rtt server socket connection
    """
    def retrieveRttData(self):
        while True:
            time.sleep(0.05)
            data = self.socket.recv(1024).decode()  # receive response
            if(len(data) > 0):
                try:
                    self.data_queue[1].put((data,))
                    self.logger.debug(data)
                    # print(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
