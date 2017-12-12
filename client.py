##
# -*- coding: utf-8 -*-
# Client.py, A Client handler for Swiftchat Websocket chat server
##
import websockets
import asyncio
import signal
import time
import json
import sys
from terminal import IO
from pprint import pformat
##
loop = asyncio.get_event_loop()
signal.signal(signal.SIGINT, signal.SIG_DFL)
##


def jsonify(data):
    return json.dumps(data)


class Client:
    def __init__(self, io):
        self.io = io
        self.exceptions = []
        self.flipped = False
        self.prefix = '>'

    async def recieve(self, websocket):
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=100)
                if response is not None:
                    response = json.loads(response)
                    op, data = response.values()
                    msg = self.io.stream_get(till_last='\n')
                    self.io.clean_line()
                    if op == 0:
                        if data['content'] == 'login as: ':
                            self.io.print(data['content'], stream='response', end='')
                        else:
                            user, content = response['d']['author'], response['d']['content']
                            self.io.print(user+': '+content, stream='response', end='\n')
                    else:
                        self.cache = response
                    self.io.print(self.prefix, stream='prefix')
                    self.io.print(msg)
                    if msg:
                        self.flipped = True
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                self.exceptions.append((str(e), int(time.time())))
                sys.exit()

    async def input(self, websocket):
        try:
            while True:
                await asyncio.sleep(0.1)
                if self.io.kbhit():
                    char = self.io.getch()
                    if char is self.io._backspace:
                        self.io.backspace()
                    elif char is self.io._return:
                        msg = self.io.stream_get(till_last='\n')
                        if self.flipped:
                            msg = ''.join(reversed(msg))
                            self.flipped = False
                        await websocket.send(jsonify({'op': 1, 'd': {'content': msg}}))
                        self.io.clean_line()
                        self.io.print(self.prefix, stream='prefix')
                    else:
                        self.io.print(char)
        except KeyboardInterrupt:
            print(self.io.clear)
            sys.exit()

    async def run(self, host='localhost', port=8765):
        try:
            destination = 'ws://{0}:{1}'.format(host, port)
            async with websockets.connect(destination) as websocket:
                asyncio.ensure_future(self.recieve(websocket))
                await self.input(websocket)
        except Exception as e:
            self.exceptions.append((str(e), int(time.time())))


def main():
    io = IO()
    client = Client(io)
    loop.run_until_complete(client.run())


if __name__ == '__main__':
    main()
