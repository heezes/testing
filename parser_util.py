import time
import threading

#":;<=>?@"
UNLOCK_OPCODE   = "UNLOCKED"#":::"
LOCK_OPCODE     = "LOCKED"#";;;"
SYNC_TRIGGERED  = "Sync Task Triggered"
SYNC_ENDED      = "Sync Task Finished"
OTA_SUCCES      = ""

TOTAL_RESPONSES =   5

LOCK_RESPONSE               =   0
UNLOCK_RESPONSE             =   1
SYNC_TRIGGERED_RESPONSE     =   2
SYNC_ENDED_RESPONSE         =   3
OTA_SUCCES_RESPONSE         =   3



class response_parser():
    def __init__(self):
        self.responseArray = {}
        for i in range(TOTAL_RESPONSES):
            self.responseArray[i].event_obj = threading.Event()

    def log_and_parse(self, queue):
        if(queue.empty() == False):
            data = queue.get()
            response_string = str(data[0])
            # resp = response_string+"  %d"%response_string.find(UNLOCK_OPCODE)
            # print(resp)
            if(response_string.find(UNLOCK_OPCODE) > -1):
                self.responseArray[UNLOCK_RESPONSE].event_obj.set()
            elif (response_string.find(LOCK_OPCODE) > -1):
                self.responseArray[LOCK_RESPONSE].event_obj.set()
            elif (response_string.find(SYNC_TRIGGERED) > -1):
                self.responseArray[SYNC_TRIGGERED_RESPONSE].event_obj.set()
            elif (response_string.find(SYNC_ENDED) > -1):
                self.responseArray[SYNC_ENDED_RESPONSE].event_obj.set()
            elif (response_string.find(OTA_SUCCES) > -1):
                self.responseArray[OTA_SUCCES_RESPONSE].event_obj.set()


    def getUnlockResult(self, wait_time):
        if(self.responseArray[UNLOCK_RESPONSE].event_obj.wait_time(wait_time) == True):
            return True
        return False

    def getLockResult(self, wait_time):
        if(self.responseArray[LOCK_RESPONSE].event_obj.wait_time(wait_time) == True):
            return True
        return False

    def getSyncResult(self, wait_time):
        if(self.responseArray[SYNC_TRIGGERED_RESPONSE].event_obj.wait_time(wait_time) == True):
            if(self.responseArray[SYNC_ENDED_RESPONSE].event_obj.wait_time(wait_time) == True):
                return True
        return False