import logging
import os

import tornado
import tornado.ioloop
import tornado.web

from handler_web import MainHandler
from handler_ws import OpenPortDetecionWebSocket


application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/ws", OpenPortDetecionWebSocket),
    ],
    autoreload=True,

    # templates
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    compiled_template_cache=False,

    # static files
    static_hash_cache=False,
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
)


if __name__ == "__main__":
    tornado.log.app_log.setLevel(logging.INFO)
    tornado.log.access_log.setLevel(logging.INFO)
    application.listen(9999)
    try:
        print("App started on port 9999")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
