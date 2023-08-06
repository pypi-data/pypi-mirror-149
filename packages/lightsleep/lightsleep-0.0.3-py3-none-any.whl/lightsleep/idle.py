import time
from .hook import Hook

class IdleSleep(Hook):
    name = 'idle'
    def sleep(self, seconds):
        time.sleep(seconds)

