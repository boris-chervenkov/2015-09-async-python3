import socket
import time
from collections import Counter
from bg_webservers_common import get_hosts, HTTP_REQUEST_TEMPLATE, detect_webserver_from_response

MAX_BYTES_TO_READ = 2048


def main():
    webservers = Counter()
    t = time.time()
    for host in get_hosts():
        get_webserver_for_host(host, webservers)

    print("Done in {}sec".format(time.time() - t))
    print(str(webservers))


def get_webserver_for_host(hostname: str, webservers: Counter):
    connection = socket.create_connection((hostname, 80), timeout=5)
    http_request_string = HTTP_REQUEST_TEMPLATE.format(hostname)
    connection.send(http_request_string.encode())
    result = connection.recv(MAX_BYTES_TO_READ)
    server = detect_webserver_from_response(result)
    webservers[server] += 1
    connection.close()
    print("Completed: {}".format(hostname))


if __name__ == "__main__":
    main()
