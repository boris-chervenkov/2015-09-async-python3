import asyncio
import time
from collections import Counter
from bg_webservers_common import get_hosts, HTTP_REQUEST_TEMPLATE, detect_webserver_from_response

TIMEOUT = 10
MAX_BYTES_TO_READ = 2048


@asyncio.coroutine
def main():
    webservers = Counter()
    running_coroutines = []
    t = time.time()
    for host in get_hosts():
        c = get_webserver_for_host(host, webservers)
        running_coroutines.append(c)

    yield from asyncio.gather(*running_coroutines)
    print("Done in {}sec".format(time.time() - t))
    print(str(webservers))


@asyncio.coroutine
def get_webserver_for_host(hostname: str, webservers: Counter):
    try:
        reader, writer = yield from asyncio.wait_for(asyncio.open_connection(host=hostname, port=80), timeout=TIMEOUT)
        http_request_string = HTTP_REQUEST_TEMPLATE.format(hostname)
        writer.write(http_request_string.encode())
        response = yield from asyncio.wait_for(reader.read(MAX_BYTES_TO_READ), timeout=TIMEOUT)
        server = detect_webserver_from_response(response)
        webservers[server] += 1
        writer.close()
        print("Completed: {}".format(hostname))
    except asyncio.TimeoutError:
        print("Timed out: {}".format(hostname))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
