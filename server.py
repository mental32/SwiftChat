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

def decode(data):
    try:
        data = json.loads(data)
        return data
    except json.decoder.JSONDecodeError:
        return None

class User:
    def __init__(self, websocket):
        self.ws = websocket
        self.name = None
        self.room = None

class Room:
    def __init__(self, name):
        self.name = name
        self.created_at = int(time.time())
        self.bucketable = 'created_at locked name'.split()
        self.sockets = set()
        self.password = None
        self.locked = False
        self.history = []

    @property
    def json(self):
        return json.dumps(self.bucket)

    @property
    def bucket(self):
        return {k: getattr(self, k) for k in self.bucketable}

    async def broadcast(self, message):
        for ws in self.sockets:
            await ws.send(jsonify(op=0, d=message))

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
            await websocket.send(
                jsonify(op=0,
                        d='Connected to {0}:{1}'.format(self.host, self.port)
                        )
                )
            await websocket.send(jsonify(op=0, d='Username: '))
            while user.name is None:
                data = await websocket.recv()
                data = decode(data)
                if data is None:
                    continue
                elif data.get('op') is 0 and data.get('d'):
                    print('DATA')
                    room = self.rooms.get('general', self.rooms[tuple(self.rooms)[0]])
                    user.name = data['d']
                    user.room = room
                    room.sockets.add(user.ws)
                    await room.broadcast(user.name+' Has entered the room!')
                    print(f'User: {user.name} has enetered into room: {user.room.name}')
                else:
                    continue

            while True:
                data = await websocket.recv()
                data = decode(data)
                if data is None:
                    continue
                elif data.get('op') is 0 and data.get('d'):
                    for ws in self.sockets:
                        await ws.send(jsonify(op=0, d=data.get('d')))
                        ack = decode(await ws.recv())
                        if ack is None:
                            continue
                        elif ack.get('op') is 1 and ack.get('d') != 'ACK':
                            await ws.send(jsonify(op=0, d=data))

        except Exception as e:
            print(str(e))

        finally:
            self.sockets.remove(websocket)
            if user.room:
                user.room.sockets.remove(user.ws)
                await user.room.broadcast(user.name+' Has left the room')
            print(f'Dropped connection: {id(websocket)}')

    def serve(self, **kwargs):
        s1 = websockets.serve(self.handler, self.host, self.port)
        self.loop.run_until_complete(s1)
        print('Serving')
        self.loop.run_forever()


def main():
    try:
        server = Server(loop)
        server.serve()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
