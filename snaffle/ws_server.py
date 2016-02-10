import multiprocessing

# Tornado
# http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.gen
import tornado.queues
import queue
import os

from snaffle.snaffle import logger

SHUTDOWN = "***SHUTDOWN***"

class StaticContentsHandler(tornado.web.RequestHandler):
    def get(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        with open('{0}/web/index.html'.format(dirname), 'rb') as f:
            self.write(f.read())


websockets = []

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    logger.debug('connection opened...')
    websockets.append(self)

  def on_message(self, message):
    logger.debug('received: {0}'.format(message))

  def on_close(self):
    logger.debug('connection closed...')
    websockets.remove(self)


application = tornado.web.Application([
  (r'/index', StaticContentsHandler),
  (r'/ws', WSHandler),
])


msg_queue = multiprocessing.Queue()

def write_something(msg):
    msg_queue.put_nowait(msg)
    # time.sleep(1)


@tornado.gen.coroutine
def process_outbound_messages(msg_queue):
    while True:
        if websockets:
            break
        yield tornado.gen.sleep(1)

    while True:
        try:
            item = msg_queue.get_nowait()
            if item == SHUTDOWN:
                exit(0)
            for s in websockets:
                s.write_message(str(item))
        except queue.Empty:
            yield tornado.gen.sleep(0.01)
        finally:
            # msg_queue.task_done()
            pass
    logger.debug("exiting loop")


def run(msg_queue):
    # TODO: use random port; http://stackoverflow.com/questions/9536531/bind-tornado-webserver-on-random-port
    application.listen(9999)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.make_current()
    ioloop.spawn_callback(process_outbound_messages, msg_queue)

    while True:
        try:
            ioloop.start()
        except KeyboardInterrupt:
            # This process should not be interrupted
            pass

process = None

def start_server_tornado():
    global process
    process = multiprocessing.Process(target=run, args=(msg_queue, ), daemon=True)
    process.start()


def shutdown():
    write_something(SHUTDOWN)
    process.join()
