##
# -*- coding: utf-8 -*-
# Client.py, A Client handler for Swiftchat Websocket chat server
##
import websockets
import asyncio
import time
import sys
from terminal import Border
##
loop = asyncio.get_event_loop()
##


class Client:
    def __init__(self, io):
        self.io = io
        self.io.border()
        self.exceptions = []
        self.messages = [None for i in range(0, self.io.resolution[1]-2)]

    async def recieve(self, websocket):
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=0.05)
                if response is not None:
                    for i, m in enumerate(self.messages):
                        if m is not None:
                            self.messages[i] = response.split('\n')[0][self.io.resolution[1]-3]
                            self.io.print(self.messages[i], x=5, y=2, stream='response')
                            break
                        continue
                    self.io.mv_cursor(*self.io.input_line)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                self.exceptions.append((str(e), int(time.time())))
                break

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
                        self.io.print(char)
        except KeyboardInterrupt:
            print(self.io.clear)
            sys.exit()

    async def run(self, host='localhost', port=8765):
        try:
            destination = 'ws://{0}:{1}'.format(host, port)
            async with websockets.connect(destination) as websocket:
                # asyncio.ensure_future(self.recieve(websocket))
                await self.input(websocket)
        except Exception as e:
            self.exceptions.append((str(e), int(time.time())))


def main():
    io = Border()
    client = Client(io)
    try:
        loop.run_until_complete(client.run())
    except KeyboardInterrupt:
        print(io.clear)
        sys.exit()
    print(io.clear)
    from pprint import pprint
    pprint(client.exceptions)


if __name__ == '__main__':
    main()
