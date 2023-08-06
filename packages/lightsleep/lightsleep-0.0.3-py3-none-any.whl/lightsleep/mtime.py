import time
import os
from .hook import Hook

class MtimeSleep(Hook):
    name = 'mtime'
    
    args = {
        'path': '/tmp/lightsleep',
        'period': '0.1'
    }

    def __init__(self, arglist):

        super().__init__(arglist)
        self.path = self.args['path']
        self.period = float(self.args['period'])


    def sleep(self, seconds):

        def mtimenone(path):
            try:
                return os.path.getmtime(self.path)
            except FileNotFoundError:
                return None

        stoptime = time.time() + seconds
        mtime_orig = mtimenone(self.path)

        while time.time() < stoptime:
            mtime = mtimenone(self.path)
            if mtime != mtime_orig:
                return
            time.sleep(self.period)
