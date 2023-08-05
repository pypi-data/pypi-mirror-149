from datetime import datetime
import time

class NexusValue:
    uid: str
    value: float

    def __init__(self, Uid, Value, timestamp=time.mktime(datetime.now().timetuple())):
        self.uid = Uid
        self.value = Value
        self.timeStamp = timestamp


    def __repr__(self):
        return f"[uid: {self.uid}, value: {self.value}]"
    

