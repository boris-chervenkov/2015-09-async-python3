import re
import os

HTTP_REQUEST_TEMPLATE = 'OPTIONS / HTTP/1.1\nHost: {}\nConnection: close\n\n'
RE_SERVER = re.compile(r'Server: (.+?)[/\r\n]', re.I)


def get_hosts():
    with open(os.path.dirname(__file__) + '/bgsites.txt', 'r') as f:
        for host in f:
            host = host.strip()
            if not host.startswith('#'):
                yield host


def detect_webserver_from_response(http_response: bytes) -> str:
    http_response = http_response.decode(errors='ignore') if isinstance(http_response, bytes) else http_response
    found_server = RE_SERVER.findall(http_response)
    return found_server[0] if found_server else None
