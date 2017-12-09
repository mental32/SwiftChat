##
import websockets
# import datetime
import asyncio
import signal
import time
import json
# import sys
# import os
##
loop = asyncio.get_event_loop()
signal.signal(signal.SIGINT, signal.SIG_DFL)
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
        self.remote_address = websocket.remote_address
        self.ip = self.remote_address[0]
        self.name = None
        self.room = None

    def __str__(self):
        return str(self.name or self.ip)


class Room:
    def __init__(self, name):
        self.name = name
        self.created_at = int(time.time())
        self.bucketable = 'created_at locked name'.split()

        self.locked = False
        self.password = None

        self.sockets = set()
        self.bans = set()
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

    async def ban(self, user):
        # ips = {ws.remote_address[0]: ws for ws in self.sockets}
        self.bans.add(user.ip)
        self.sockets.remove(user.ws)
        await user.ws.send(jsonify(op=1, d={'avaliable': False, 'room': self.name}))


class Server:
    def __init__(self, loop):
        self.rooms = {
            'general': Room(name='general'),
            'irc': Room(name='irc'),
        }
        self.host = 'localhost'
        self.port = 8765
        self.sockets = set()
        self.users = set()
        self.loop = loop

    @property
    def connected_to(self):
        return 'Connected to {0}:{1}'.format(self.host, self.port)

    async def handler(self, websocket, path):
        try:
            self.sockets.add(websocket)
            print('Connection added:', id(websocket), websocket.remote_address)
            user = User(websocket)
            await websocket.send(jsonify(op=0, d=self.connected_to))
            await websocket.send(jsonify(op=0, d='Username: '))
            while user.name is None:
                data = await websocket.recv()
                data = decode(data)
                if data is None:
                    continue
                elif data.get('op') is 0 and data.get('d'):
                    first_room = self.rooms[tuple(self.rooms)[0]]
                    room = self.rooms.get('general', first_room)
                    user.name = data['d']
                    user.room = room
                    room.sockets.add(user.ws)
                    await room.broadcast(user.name+' Has entered the room!')
                else:
                    continue

            while True:
                asyncio.sleep(0.1)
                data = decode(await websocket.recv())
                print(data)
                if data is None:
                    continue
                elif data.get('op') is 0 and data.get('d'):
                    for ws in user.room.sockets:
                        await ws.send(jsonify(op=0, d=data.get('d')))

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
