##
import websockets
import datetime
import asyncio
import time
import json
import sys
import os
##
loop = asyncio.get_event_loop()
##

def jsonify(op, d):
    return json.dumps({'op': op, 'd': d})

class User:
    def __init__(self, websocket):
        self.ws = websocket
        self.name = None
        self.room = None

class Room:
    def __init__(self, name):
        self.created_at = int(time.time())
        self.sockets = set()
        self.history = []
        self.locked = False
        self.password = None
        self.name = name
        self.bucketable = 'created_at locked name'.split()

    @property
    def json(self):
        return json.dumps(self.bucket)

    @property
    def bucket(self):
        return {k: getattr(self, k) for k in self.bucketable}

    async def broadcast(self, message):
        for ws in self.sockets:
            await ws.send(message)

class Server:
    def __init__(self, loop):
        self.rooms = {
            'general': Room(name='general'),
        }
        self.host = 'localhost'
        self.port = 8765
        self.sockets = set()
        self.users = set()
        self.loop = loop

    async def handler(self, websocket, path):
        try:
            self.sockets.add(websocket)
            print(f'Connection added: {id(websocket)}')
            user = User(websocket)
            await websocket.send('Connected to {0}:{1}'.format(self.host, self.port))
            while user.name is None:
                await websocket.send('Username: ')
                print('Loop')
                d = await websocket.recv()
                if d.strip():
                    room = self.rooms.get('general', self.rooms[tuple(self.rooms)[0]])
                    user.name = d
                    user.room = room
                    room.sockets.add(user.ws)
                    await room.broadcast(user.name+' Has entered the room!')
                    print(f'User: {user.name} has enetered into room: {user.room.name}')
                else:
                    continue

            while True:
                d = await websocket.recv()
                if d:
                    print(d)
                    for ws in self.sockets:
                        print(ws)
                        await ws.send(d)

        except Exception as e:
            print(str(e))
        finally:
            self.sockets.remove(websocket)
            user.room.sockets.remove(user.ws)
            print(f'Dropped connection: {id(websocket)}')

    def serve(self, **kwargs):
        s1 = websockets.serve(self.handler, self.host, self.port)
        self.loop.run_until_complete(s1)
        print('Serving')
        self.loop.run_forever()


if __name__ == '__main__':
    server = Server(loop)
    server.serve()