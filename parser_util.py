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
    """
    @brief: This function should be called continuously to dequeue and parse the log data
    @param: queue: Byte array which contains rtt log data from target
    """
    def log_and_parse(self, queue):
        if(queue.empty() == False):
            data = queue.get()
            response_string = str(data[0])
            # print(response_string)
            if(response_string.find(UNLOCK_OPCODE) > -1):
                self.event_obj[UNLOCK_RESPONSE].set()
                print("***Unlock Response Received***")
            elif (response_string.find(LOCK_OPCODE) > -1):
                self.event_obj[LOCK_RESPONSE].set()
                print("***Lock Response Received***") 
            elif (response_string.find(SYNC_TRIGGERED) > -1):
                self.event_obj[SYNC_TRIGGERED_RESPONSE].set()
                print("***Sync Trigger Response Received***") 
            elif (response_string.find(SYNC_ENDED) > -1):
                self.event_obj[SYNC_ENDED_RESPONSE].set()
                print("***Sync End Response Received***")
            else:
                pass
            # elif (response_string.find(OTA_SUCCES) > -1):
            #     self.event_obj[OTA_SUCCES_RESPONSE].set()
            #     print("***Ota Response Received***")
    """
    @brief: This function should be called to check if the unlock request succeded
    @param: wait_time: Time to wait for the response (seconds)
    """
    def getUnlockResult(self, wait_time):
        if(self.event_obj[UNLOCK_RESPONSE].wait(wait_time) == True):
            self.event_obj[UNLOCK_RESPONSE].clear()
            return True
        return False
    """
    @brief: This function should be called to check if the lock request succeded
    @param: wait_time: Time to wait for the response (seconds)
    """
    def getLockResult(self, wait_time):
        if(self.event_obj[LOCK_RESPONSE].wait(wait_time) == True):
            self.event_obj[LOCK_RESPONSE].clear()
            return True
        return False
    """
    @brief: This function should be called to monitor the starting and ending of the sync task
    @param: wait_time: Time to wait for the response (seconds)
    """
    def getSyncResult(self, wait_time):
        if(self.event_obj[SYNC_TRIGGERED_RESPONSE].wait(wait_time) == True):
            if(self.event_obj[SYNC_ENDED_RESPONSE].wait(wait_time) == True):
                self.event_obj[SYNC_TRIGGERED_RESPONSE].clear()
                self.event_obj[SYNC_ENDED_RESPONSE].clear()
                return True
        return False