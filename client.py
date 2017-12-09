##
# -*- coding: utf-8 -*-
# Client.py, A Client handler for Swiftchat Websocket chat server
##
import websockets
import asyncio
import time
import sys
from terminal import (Border, IO)
##
loop = asyncio.get_event_loop()
##


class Client:
    def __init__(self, io):
        self.io = io
        self.exceptions = []

    async def recieve(self, websocket):
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=0.05)
                if response is not None:
                    cols, rows = self.io.resolution
                    msg = self.io.stream_get(till_last='\n')
                    self.io.clean_line()
                    self.io.print(response[:cols-3], stream='response', end='\n')
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
                        await websocket.send(msg)
                        self.io.clean_line()
                    elif char == ':':
                        pass
                    else:
                        # self.io.streams['main'].append(char)
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
