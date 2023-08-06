import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import websockets
import ssl

import requests

import pickle

import random
import string
from functools import partial

import time

import logging
logging.getLogger('werkzeug').disabled = True

import os

print_verbose = lambda s: print(f"--CommunicationHandler-- : {s}" )

try:
    from flask import Flask
    from flask import request
    from gevent.pywsgi import WSGIServer
except ImportError:
    logging.debug("flask/gevent not found - only websocket servers can be spawned (\'send\' not affected)")
    pass

class CommunicationHandler():
    def __init__(self, protocol='websocket', cert_path=None, num_retry=3, verbose=True, resp_store_duration=120):
        self.protocol = protocol
        self.msg_queues = {}
        self.resp_queue = {}
        self.resp_cache = {}

        self.num_retry = num_retry

        self.resp_store_duration = resp_store_duration

        self.verbose = verbose

        self.ssl = False
        self.ssl_context = None

        if cert_path is not None:
            self.cert_path = cert_path
            self.ssl = True

            if self.protocol == 'websocket':
                self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                self.ssl_context.load_cert_chain(certfile=self.cert_path)

        self.servers = []

    async def send(self, msg, addr):
        if self.protocol == 'websocket':
            url = f"{('wss' if self.ssl else 'ws')}://{addr}"

            async with websockets.connect(url, max_size=None, max_queue=None, ping_interval=None, ssl=self.ssl_context) as websocket:
                await websocket.send(msg)
                resp = pickle.loads(await websocket.recv())
                return resp

        elif self.protocol == 'http':
            url = f"{'https' if self.ssl else 'http'}://{addr}"

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(2) as pool:
                encoded_resp = await loop.run_in_executor(pool, partial(requests.post, url=url, data=msg, verify=(self.cert_path if self.ssl else True)))
                resp = pickle.loads(encoded_resp.content)
                return resp

    async def send_msg(self, msg, addr, resp_required = True):
        # Generate random 16-char id
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        encoded_msg = pickle.dumps((id, msg))

        for attempt in range(self.num_retry):
            try:
                send_resp = await self.send(encoded_msg, addr)
            except:
                if (self.num_retry - attempt < 1):
                    if self.verbose: print_verbose(f'Send attempt {attempt} failed for message {id}')
                    continue
                else:
                    logging.error(f"Failed to send message after {self.num_retry} attempts")
                    raise
            else:
                break

        if self.verbose: print_verbose(f'Message sent: {msg}')

        if (resp_required):
            for attempt in range(self.num_retry):
                try:
                    msg_resp = await self.poll_msg_resp(addr, id)
                except:
                    if (self.num_retry - attempt < 1):
                        if self.verbose: print_verbose(f'Receive response attempt {attempt} failed for message {id}')
                        continue
                    else:
                        logging.error(f"Failed to receive response after {self.num_retry} attempts")
                        raise
                else:
                    if self.verbose: print_verbose(f'Response received: {msg_resp}')
                    return msg_resp
        else:
            return send_resp

    async def poll_msg_resp(self, addr, id):
        encoded_msg = pickle.dumps((id, 'POLL'))
        msg_resp = await self.send(encoded_msg, addr)

        while msg_resp == "NOT_FINISHED":
            if self.verbose: print_verbose(f"Polling for msg {id}")
            await asyncio.sleep(5)
            msg_resp = await self.send(encoded_msg, addr)

        return msg_resp

    def create_server(self, host, port):
        self.msg_queues[f'{host}:{port}'] = {}

        if self.protocol == 'websocket':
            self.servers.append(WSServerHandler(host, int(port), self.msg_queues, self.resp_queue, self.resp_cache, self.ssl_context))
        else:
            self.servers.append(HTTPServerHandler(host, int(port), self.msg_queues, self.resp_queue, self.resp_cache, self.ssl_context))
        if self.verbose: print_verbose('Server created')

    def _start_ws_servers(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(asyncio.gather(
            *[websockets.serve(s.parse_msg, s.host, s.port, max_size=None, max_queue=None, ping_interval=None, ssl=s.ssl_context) for s in self.servers])
        )
        loop.run_forever()

    def start_servers(self):
        if self.verbose: print_verbose('Servers started')
        if self.protocol == 'websocket':
            self.server_thread = Thread(target=self._start_ws_servers)
            self.server_thread.start()
        elif self.protocol == 'http':
            self.server_threads = [Thread(target=s.start_server) for s in self.servers]
            for th in self.server_threads:
                th.start()

        self.start_resp_cache_cleaner()

    async def get_msg(self, addr):
        while (len(self.msg_queues[addr]) == 0):
            await asyncio.sleep(5)
        if self.verbose: print_verbose(self.msg_queues)

        msg_id = list(self.msg_queues[addr])[0]
        msg_entry = self.msg_queues[addr].pop(msg_id)
        if self.verbose: print_verbose("Message popped from queue")

        return msg_entry, msg_id

    def push_msg_resp(self, resp, id):
        self.resp_queue[id] = resp
        if self.verbose: print_verbose("Response added to queue")

    def start_resp_cache_cleaner(self):
        self.cleaner_thread = Thread(target=self._clean_resp_cache)
        self.cleaner_thread.start()

    def _clean_resp_cache(self):
        while True:
            while (len(self.resp_cache) == 0):
                time.sleep(3)
            msg_id = list(self.resp_cache)[0]
            msg_time = self.resp_cache[msg_id][1]
            while (time.mktime(time.gmtime()) - time.mktime(msg_time) < self.resp_store_duration):
                time.sleep(3)
            self.resp_cache.pop(msg_id)


class HTTPServerHandler():
    def __init__(self, host, port, msg_queues, resp_queue, resp_cache, ssl_context):
        self.host = host
        self.port = port

        self.msg_queues = msg_queues
        self.resp_queue = resp_queue
        self.resp_cache = resp_cache

        self.ssl_context = ssl_context

        self.flask_server = Flask(f"CommunicationHandler HTTP Server - {self.port}")
        self.flask_server.logger.disabled = True
        self.flask_server.add_url_rule('/', view_func=self.parse_msg, methods=['POST'])

    def start_server(self):
        # self.flask_server.run(host=self.host, port=self.port, ssl_context=self.ssl_context)
        WSGIServer((self.host, self.port), self.flask_server, log=None).serve_forever()

    def parse_msg(self):
        encoded_msg = request.data
        id, msg = pickle.loads(encoded_msg)

        if msg == 'POLL':
            if id in self.resp_queue:
                resp = pickle.dumps(self.resp_queue[id])
                self.resp_cache[id] = (self.resp_queue[id], time.gmtime())
                self.resp_queue.pop(id)
                return resp
            elif id in self.resp_cache:
                resp = pickle.dumps(self.resp_cache[id])[0]
                return resp
            else:
                return pickle.dumps("NOT_FINISHED")
        else:
            self.msg_queues[f'{self.host}:{self.port}'][id] = msg
            return pickle.dumps("ACK")


class WSServerHandler():
    def __init__(self, host, port, msg_queues, resp_queue, resp_cache, ssl_context):
        self.host = host
        self.port = port

        self.msg_queues = msg_queues
        self.resp_queue = resp_queue
        self.resp_cache = resp_cache

        self.ssl_context = ssl_context

    async def parse_msg(self, websocket, path):
        encoded_msg = await websocket.recv()
        id, msg = pickle.loads(encoded_msg)

        if msg == 'POLL':
            if id in self.resp_queue:
                await websocket.send(pickle.dumps(self.resp_queue[id]))
                self.resp_cache[id] = (self.resp_queue[id], time.gmtime())
                self.resp_queue.pop(id)
            elif id in self.resp_cache:
                await websocket.send(pickle.dumps(self.resp_cache[id])[0])
            else:
                await websocket.send(pickle.dumps("NOT_FINISHED"))
        else:
            self.msg_queues[f'{self.host}:{self.port}'][id] = msg
            await websocket.send(pickle.dumps("ACK"))
