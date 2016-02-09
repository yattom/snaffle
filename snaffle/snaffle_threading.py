# coding: utf-8

import time
import logging
import threading
import webbrowser
from autobahn.asyncio.websocket import WebSocketServerProtocol

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Tornado
# http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.gen
import tornado.queues

class StaticContentsHandler(tornado.web.RequestHandler):
    def get(self):
        with open('web/index.html', 'rb') as f:
            self.write(f.read())


websockets = []

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    logger.debug('connection opened...')
    websockets.append(self)
    # self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
    logger.debug('received: {0}'.format(message))
    cmd = '''
    {
      "type": "script",
      "content": "ctx.beginPath(); ctx.moveTo(20, 20); ctx.lineTo(120, 20); ctx.lineTo(120, 120); ctx.lineTo(20, 120); ctx.closePath(); ctx.stroke();"
    }
    '''
    self.write_message(cmd)

  def on_close(self):
    logger.debug('connection closed...')
    websockets.remove(self)

  def check_origin(self, origin):
      return True


application = tornado.web.Application([
  (r'/index', StaticContentsHandler),
  (r'/ws', WSHandler),
])


msg_queue = tornado.queues.Queue()

def write_something(msg):
    msg_queue.put_nowait(msg)
    time.sleep(0.01)


async def process_outbound_messages():
    async for item in msg_queue:
        try:
            for s in websockets:
                s.write_message(str(item))
        finally:
            msg_queue.task_done()


def start_server_tornado():
    def run():
        # TODO: use random port; http://stackoverflow.com/questions/9536531/bind-tornado-webserver-on-random-port
        application.listen(9999)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.make_current()
        ioloop.spawn_callback(process_outbound_messages)
        ioloop.start()
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def init():
    start_server_tornado()
    webbrowser.open('http://localhost:9999/index')

    class Context:
        pass

    ctx = Context()
    ctx.write_something = write_something
    return ctx


