# coding: utf-8

import time
import logging
import webbrowser

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

import snaffle.ws_server

class Snaffle:
    def __init__(self, start=True):
        if start:
            self.start()

    def start(self):
        snaffle.ws_server.start_server_tornado()
        webbrowser.open('http://localhost:9999/index')

    def shutdown(self):
        snaffle.ws_server.shutdown()

    def write_something(self, msg):
        snaffle.ws_server.write_something(msg)

    def send_script(self, script):
        msg = '''
        {{
          "type": "script",
          "content": "{0}"
        }}
        '''.format(script)
        self.write_something(msg)
