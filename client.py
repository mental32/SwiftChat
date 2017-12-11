##
# -*- coding: utf-8 -*-
# Client.py, A Client handler for Swiftchat Websocket chat server
##
import websockets
import asyncio
import time
import json
import sys
from terminal import IO
from pprint import pformat
##
loop = asyncio.get_event_loop()
##


def jsonify(data):
    return json.dumps(data)


class Client:
    def __init__(self, io):
        self.io = io
        self.exceptions = []
        self.prefix = '>'

    async def recieve(self, websocket):
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=1)
                if response is not None:
                    response = json.loads(response)
                    cols, rows = self.io.resolution
                    msg = self.io.stream_get(till_last='\n')
                    self.io.clean_line()
                    if response['op'] == 0:
                        if response['d']['content'] == 'login as: ':
                            self.io.print(response['d']['content'], stream='response', end='')
                        else:
                            user, content = response['d']['author'], response['d']['content']
                            self.io.print(user+': '+content, stream='response', end='\n')
                    else:
                        self.cache = response
                    self.io.print(self.prefix, stream='prefix')
                    self.io.print(msg)
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
    try:
        loop.run_until_complete(client.run())
    except KeyboardInterrupt:
        print(io.clear)
        sys.exit()
    print(client.exceptions)


if __name__ == '__main__':
    main()
