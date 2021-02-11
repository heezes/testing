import pygatt
import time
from binascii import hexlify
import sys

class interface():
    def __init__(self, data_queue, ble_interface=True):
        #intialize the vim response mechanism
        self.device = 0
        self.data_queue = []
        self.data_queue.append(data_queue[0])
        self.data_queue.append(data_queue[1])
        self.ble_interface = interface #Use BLE interface
        self.opcode_response = None #BLE opcode response for a command
        self.connectToInterface(interface)

    def data_handler_cb(self, handle, value):
        try:
            self.opcode_response = value.decode("utf-8")
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


    def received_data_cb(self, handle, value):
        try:
            data = value.decode("utf-8")
            # print(data)
            # self.data_queue[0].put((data,))
            self.data_queue[1].put((data,))
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    def Disconnected(self):
        print ("disconnected from BLE")

    def connectToInterface(self, interface):
        if(self.ble_interface):
            adapter = pygatt.GATTToolBackend(search_window_size=200)
            adapter.start()
            self.device = adapter.connect("EC:25:3D:28:F1:EA", address_type = pygatt.BLEAddressType.random, auto_reconnect=True)
            self.device.register_disconnect_callback(self.Disconnected)
            self.device.exchange_mtu(128)
            self.device.subscribe("ed0ef62e-9b0d-11e4-89d3-123b93f75eba",\
                            callback=self.data_handler_cb,\
                            indication=False)
            self.device.subscribe("ed0ef62e-9b0d-11e4-89d3-123b93f75fba",\
                            callback=self.received_data_cb,\
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
        # else:
            #add other interface initialization

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