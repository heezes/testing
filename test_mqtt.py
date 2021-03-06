import paho.mqtt.client as mqtt
import time
import sys
import json

SUBSCRIPTION_TOPIC  =   "vim/subscribe"
DEBUG_PUBLISH_TOPIC =   "vim/debug_publish"
INFO_PUBLISH_TOPIC  =   "vim/info_publish"
class Mqtt():
    def __init__(self, queue):
        self.queue = queue
        self.test_request = 0
        self.test_arg = [1,2,3,4,5] #[mode, wait_time, count, timeout, ...]
        self.test_commit_msg = ""
        self.mqttc  = mqtt.Client()
        self.mqttc.username_pw_set(username='munnvxsn', password='unegqTSYxMKO')
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_disconnect = self.on_disconenct
        self.mqttc.connect_async("m11.cloudmqtt.com", 19845, 60)
        self.mqttc.loop_start()

    # def connectionManage(self):
    #     while(True):
    #         if(self.mqttc.is_connected()):
    #             if(self.queue.empty() == False):
    #                 data = []
    #                 try:
    #                     data = self.queue.get()
    #                     print(str(data[0]))
    #                     self.mqttc.publish(DEBUG_PUBLISH_TOPIC, str(data[0]), qos=1)
    #                 except Exception as e:
    #                     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    #         elif (self.mqttc.is_connected() == False):
    #             try:
    #                 self.mqttc.connect_async("m11.cloudmqtt.com", 19845, 60)
    #                 self.mqttc.loop_start()
    #                 while(self.mqttc.is_connected() == False):
    #                     pass
    #             except:
    #                 self.mqttc.loop_stop()
    #                 self.mqtt_connected = False

    """
    @brief: Send message to the remote  mqtt server
    @param: message: Data to be sent
    """
    def sendInfo(self, message):
        self.mqttc.publish(INFO_PUBLISH_TOPIC,str(message), qos=1, retain=False)

    """
    @brief: Check the string for numeric value
    @param: s: Checks if string is numeric(atoi())
    """
    def isNumeric(self, s):
        s = s.strip()
        try:
            s = float(s)
            return True
        except:
            return False

    """
    @brief: Callback function for mqtt connection
    @param: client: client handle
    @param: userdata: data passed to user via stack
    @param: flags: mqtt flag
    @params: rc: return code
    """
    def on_connect(self, client, userdata, flags, rc):
        # self.mqtt_connected = True
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(SUBSCRIPTION_TOPIC)

    """
    @brief: Callback function when data is recieved on subscribed topic
    @param: client: client handle
    @param: userdata: data passed to user via stack
    @param: msg: data received on subscribed topic
    """
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        try:
            if(self.test_request == 0):
                self.test_arg.clear()
                request_json = json.loads(msg.payload)
                if 'cmd' in request_json:
                    self.test_request = request_json['cmd']
                if 'arg' in request_json:
                    for i in range(len(request_json['arg'])):
                        self.test_arg.append(request_json['arg'][i])
                if 'msg' in request_json:
                    self.test_commit_msg = str(request_json['msg'])
            else:
                self.test_request("Already Executing Test id: %d"%self.test_request)
        except Exception as e :
            print(e)
            pass
        # if(self.isNumeric(str(msg.payload))):
        #     self.test_request = int(msg.payload.strip())

    """
    @brief: Callback function for mqtt disconnection
    @param: client: client handle
    @param: userdata: data passed to user via stack
    @params: rc: return code
    """
    def on_disconenct(self, client, userdata, rc):
        print("Disconected with result code: "+str(rc))
        # self.mqtt_connected = False
