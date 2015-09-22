import asyncio
import time
from collections import Counter
from bg_webservers_common import get_hosts, HTTP_REQUEST_TEMPLATE, detect_webserver_from_response

MAX_BYTES_TO_READ = 2048


async def main():
    webservers = Counter()
    running_coroutines = []
    t = time.time()
    for host in get_hosts():
        c = get_webserver_for_host(host, webservers)
        running_coroutines.append(c)

    await asyncio.gather(*running_coroutines)
    print("Done in {}sec".format(time.time() - t))
    print(str(webservers))


async def get_webserver_for_host(hostname: str, webservers: Counter):
    reader, writer = await asyncio.open_connection(host=hostname, port=80)
    http_request_string = HTTP_REQUEST_TEMPLATE.format(hostname)
    writer.write(http_request_string.encode())
    response = await reader.read(MAX_BYTES_TO_READ)
    server = detect_webserver_from_response(response)
    webservers[server] += 1
    writer.close()
    print("Completed: {}".format(hostname))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
