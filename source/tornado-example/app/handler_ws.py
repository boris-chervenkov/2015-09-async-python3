from tornado import websocket
from tornado import gen
from tornado.tcpclient import TCPClient

from ports import PORTS


class OpenPortDetecionWebSocket(websocket.WebSocketHandler):

    tcp_client = TCPClient()

    @gen.coroutine
    def on_message(self, message):
        self.write_message("проверявам ... ")
        ip = self.request.remote_ip
        coroutines = []
        for port, description in PORTS.items():
            coroutines.append(self.check_open_port(ip, port, description))
        results = yield coroutines
        if any(results):
            self.write_message("- - - - - -")
            self.write_message("Готово - имаш {} отворени популярни порта :о)".format(sum(results)))
        else:
            self.write_message("Нямаш отворени популярни портове :o)")


    @gen.coroutine
    def check_open_port(self, ip, port, description):
        try:
            iostream = yield self.tcp_client.connect(host=ip, port=port)
            iostream.close()
            self.write_message("отворен порт {} - {}".format(port, description))
            print("Detected open port IP={} port={} ({})".format(ip, port, description))
            return True
        except:
            return False
