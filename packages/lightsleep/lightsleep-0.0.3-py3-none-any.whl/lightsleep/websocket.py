import time
from .hook import Hook
from .exceptions import SleepException
import os

import socketio

sio = socketio.Client()

class WebsocketSleep(Hook):
    name = 'ws'
    
    args = {
        'url': 'http://localhost:8899/',
        'room': None,
        'event': 'update',
        'secret': None,
        'data': None,
        'period': '0.1'
    }

    def __init__(self, arglist):
        super().__init__(arglist)
        self.period = float(self.args['period'])


    def sleep(self, seconds):
        self._stop = False
        stoptime = time.time() + seconds

        @sio.event
        def connect():
            sio.emit('join', {'room': self.args['room'], 'secret': self.args['secret']})

        @sio.on('*')
        def catch_all(event, data):
            # ignore if other event
            if self.args['event'] and event != self.args['event']:
                return

            # ignore if other data
            if self.args['data'] and data != self.args['data']:
                return

            self._stop = True

        sio.connect(self.args['url'])
        while time.time() < stoptime and not self._stop:
            time.sleep(self.period)
        sio.disconnect()
