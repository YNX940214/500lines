#!/usr/bin/env python3.4

"""Sloppy little crawler, demonstrates a hand-made event loop and callbacks."""

from selectors import *
import socket
import re
import urllib.parse
import time
import ssl

# 2447 URLs fetched in 342.5 seconds, achieved concurrency = 19

HOST = 'xkcd.com'
PORT = 443
urls_todo = set(['/'])
seen_urls = set(['/'])
concurrency_achieved = 0
selector = DefaultSelector()
stopped = False


class Fetcher:
    def __init__(self, url):
        self.response = b''
        self.url = url
        self.sock = None
        self.flag = True

    def do_hs(self, key, b):
        try:
            self.sock.do_handshake()
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                if self.flag:
                    selector.register(self.sock.fileno(), EVENT_WRITE | EVENT_READ, self.do_hs)
                    self.flag = False
                return
            elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                return
            elif err.args[0] in (ssl.SSL_ERROR_EOF, ssl.SSL_ERROR_ZERO_RETURN):
                return self.close(exc_info=err)
            elif err.args[0] == ssl.SSL_ERROR_SSL:
                try:
                    peer = self.sock.getpeername()
                except Exception:
                    peer = "(not connected)"
                print("SSL Error on %s %s: %s", self.sock.fileno(), peer, err)
                return self.close(exc_info=err)
            raise
        except ssl.CertificateError as err:
            print(err)
        except socket.error as err:
            print(err)
        except AttributeError as err:
            print(err)
        else:
            # print('done')
            selector.unregister(key.fd)
            selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def fetch(self):
        # print("fetch called")
        global concurrency_achieved
        concurrency_achieved = max(concurrency_achieved, len(urls_todo))

        self.sock = socket.socket()
        try:
            self.sock.connect((HOST, PORT))
        except BlockingIOError:
            pass
        self.sock = ssl.wrap_socket(self.sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23, do_handshake_on_connect=False)
        self.sock.setblocking(False)
        self.do_hs("", "")
        # selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        try:
            chunk = self.sock.recv(4096)  # 4k chunk size.
            if chunk:
                self.response += chunk
            else:
                print(self.url)

                selector.unregister(key.fd)  # Done reading.
                links = self.parse_links()
                for link in links.difference(seen_urls):
                    urls_todo.add(link)
                    Fetcher(link).fetch()

                seen_urls.update(links)
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
        except ssl.SSLError as e:
            if e.args[0] == ssl.SSL_ERROR_WANT_READ:
                return
            else:
                raise
        except BlockingIOError:
            raise
        except ConnectionResetError as e:
            print("crawling {0}  failed due to {1}".format(self.url,e))
            selector.unregister(key.fd)
            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True
            return



    def body(self):
        body = self.response.split(b'\r\n\r\n', 1)[1]
        return body.decode('utf-8')

    def parse_links(self):
        if not self.response:
            print('error: {}'.format(self.url))
            return set()
        if not self._is_html():
            return set()
        urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                              self.body()))

        links = set()
        for url in urls:
            normalized = urllib.parse.urljoin(self.url, url)
            parts = urllib.parse.urlparse(normalized)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            host, port = urllib.parse.splitport(parts.netloc)
            if host and host.lower() not in (HOST, 'www.xkcd.com'):
                continue
            defragmented, frag = urllib.parse.urldefrag(parts.path)
            links.add(defragmented)

        return links

    def _is_html(self):
        head, body = self.response.split(b'\r\n\r\n', 1)
        headers = dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
        return headers.get('Content-Type', '').startswith('text/html')


start = time.time()
fetcher = Fetcher('/')
fetcher.fetch()

while not stopped:
    events = selector.select()
    for event_key, event_mask in events:
        callback = event_key.data
        callback(event_key, event_mask)

print('{} URLs fetched in {:.1f} seconds, achieved concurrency = {}'.format(
    len(seen_urls), time.time() - start, concurrency_achieved))
