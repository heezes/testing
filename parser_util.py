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
        self.event_obj = []
        for i in range(TOTAL_RESPONSES):
            self.event_obj.append(threading.Event())

    def log_and_parse(self, queue):
        if(queue.empty() == False):
            data = queue.get()
            response_string = str(data[0])
            # resp = response_string+"  %d"%response_string.find(UNLOCK_OPCODE)
            # print(resp)
            if(response_string.find(UNLOCK_OPCODE) > -1):
                self.event_obj[UNLOCK_RESPONSE].set()
            elif (response_string.find(LOCK_OPCODE) > -1):
                self.event_obj[LOCK_RESPONSE].set()
            elif (response_string.find(SYNC_TRIGGERED) > -1):
                self.event_obj[SYNC_TRIGGERED_RESPONSE].set()
            elif (response_string.find(SYNC_ENDED) > -1):
                self.event_obj[SYNC_ENDED_RESPONSE].set()
            elif (response_string.find(OTA_SUCCES) > -1):
                self.event_obj[OTA_SUCCES_RESPONSE].set()


    def getUnlockResult(self, wait_time):
        if(self.event_obj[UNLOCK_RESPONSE].wait(wait_time) == True):
            return True
        return False

    def getLockResult(self, wait_time):
        if(self.event_obj[LOCK_RESPONSE].wait(wait_time) == True):
            return True
        return False

    def getSyncResult(self, wait_time):
        if(self.event_obj[SYNC_TRIGGERED_RESPONSE].wait(wait_time) == True):
            if(self.event_obj[SYNC_ENDED_RESPONSE].wait(wait_time) == True):
                return True
        return False