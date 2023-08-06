import time
from .hook import Hook
from .exceptions import SleepException

from .idle import IdleSleep
from .redis import RedisSleep
from .websocket import WebsocketSleep
from .mtime import MtimeSleep

class Sleep():
    """ This is unified sleep class which handles all hooks """
    def __init__(self, hook=None):
        if hook:
            self.set_hook(hook)
        else:
            self.hook = IdleSleep()

    def set_hook(self, hook):
        for sub in Hook.__subclasses__():
            if sub.name == hook[0]:
                self.hook = sub(hook[1:])
                return
            
        raise SleepException(f"Not found hook {hook[0]}")

    def sleep(self, n):
        self.hook.sleep(n)

    @staticmethod
    def hooks():
        h = dict()
        for sub in Hook.__subclasses__():
            h[sub.name] = sub.args
        
        return h

