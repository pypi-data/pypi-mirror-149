import redis
import time
from .hook import Hook

class RedisSleep(Hook):
    name = 'redis'
    
    args = {
        'url': 'redis://localhost:6379/0',
        'ch': 'sleep',
        'msg': None,
        'period': '0.1'
    }

    def __init__(self, arglist):

        super().__init__(arglist)
        self.period = float(self.args['period'])
        self.redis = redis.from_url(self.args['url'], decode_responses=True)

    def stopmsg(self, msg):
        if msg is None:
            return False

        if self.args['msg']: 
            return(self.args['msg'] == msg['data'])

        return True

    def sleep(self, seconds):
        
        stop_time = time.time() + seconds

        p = self.redis.pubsub(ignore_subscribe_messages=True)
        p.subscribe(self.args['ch'])

        while True:
            gmstart = time.time()
            msg = p.get_message(timeout = seconds)
            if self.stopmsg(msg) or time.time() >= stop_time:
                p.unsubscribe()
                return

            left = stop_time - time.time()
            time.sleep(min(self.period, left))


