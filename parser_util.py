import time

#":;<=>?@"
UNLOCK_OPCODE   = "UNLOCKED"#":::"
LOCK_OPCODE     = "LOCKED"#";;;"


class response_parser():
    def __init__(self):
        self.unlock = None
        self.lock = None

    def log_and_parse(self, queue):
        if(queue.empty() == False):
            data = queue.get()
            response_string = str(data[0])
            # resp = response_string+"  %d"%response_string.find(UNLOCK_OPCODE)
            # print(resp)
            if(response_string.find(UNLOCK_OPCODE) > -1):
                # print("UNLOCK Received")
                self.unlock = 1
            elif (response_string.find(LOCK_OPCODE) > -1):
                # print("LOCKED Received")
                self.lock = 1

    def getUnlockResult(self, wait_time):
        if(self.unlock == True):
            self.unlock = None
            return True
        else:
            #wait for the response
            time.sleep(wait_time)
            if(self.unlock == True):
                self.unlock = None
                return True
            else:
                return False

    def getLockResult(self, wait_time):
        if(self.lock == True):
            self.lock = None
            return True
        else:
            #wait for the response
            time.sleep(wait_time)
            if(self.lock == True):
                self.lock = None
                return True
            else:
                return False
