##
import websockets
# import datetime
import asyncio
import signal
import shlex
import time
import json
# import sys
# import os
import payloads
##
loop = asyncio.get_event_loop()
signal.signal(signal.SIGINT, signal.SIG_DFL)
##


def jsonify(data):
    return json.dumps(data)


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
        self.connected_at = int(time.time())
        self.name = None
        self.room = None

    def __str__(self):
        return str(self.name or 'Guest')


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
        pl = payloads.message_recieved(author='*'+self.name, content=message)
        for ws in self.sockets:
            await ws.send(jsonify(pl))

    async def ban(self, user):
        self.sockets.remove(user.ws)
        self.bans.add(user.ip)
        pl = payloads.room_state_change(avaliable=False, room=self.name)
        await user.ws.send(jsonify(pl))


class Server:
    def __init__(self, loop):
        self.rooms = {
            'NLI lobby': Room(name='NLI lobby'),
            'general': Room(name='general'),
        }
        self.command_prefix = '\\'
        self.host = 'localhost'
        self.port = 8765
        self.prefrences = {}
        self.sockets = set()
        self.users = set()
        self.loop = loop

    @property
    def connected_to(self):
        return 'Connected to {0}:{1}'.format(self.host, self.port)

    @property
    def first_room(self):
        return self.rooms[tuple(self.rooms)[0]]

    @property
    def cache(self):
        return {
            'rooms': tuple(room.bucket for room in self.rooms.values()),
            'users': tuple(str(user) for user in self.users)
            'command_prefix': self.command_prefix,
            'host': self.host,
            'port': self.port,
        }

    async def execute(self, command, user):
        op, *args = shlex.split(command)
        if op == 'switch':
            target = args[0]
            if target in self.rooms:
                room = self.rooms[target]
                if not room.locked:
                    pass
                else:
                    pass
            else:
                pass 
            # await websocket.send('Attempting to move to channel {0}'.format(args[0]))
            pass

    async def handler(self, websocket, path):
        try:
            self.sockets.add(websocket)
            user = User(websocket)
            if self.prefrences.get('motd', None):
                await websocket.send(self.prefrences['motd'])
            else:
                if self.prefrences.get('show_connected_to'):
                    await websocket.send(self.prefrences.get('connected_to', self.connected_to))

            # Login sequence
            await websocket.send(jsonify({'op': 0, 'd': {'content': 'login as: '}}))
            while user.name is None:
                data = decode(await websocket.recv())
                if data is None:
                    continue
                elif data.get('op') == 1 and data.get('d', {}).get('content'):
                    user.name = data['d']['content']
                    user.room = self.rooms.get('NLI lobby', self.first_room)
                    user.room.sockets.add(user.ws)
                    await user.room.broadcast(user.name+' Has entered the room!')
                else:
                    continue
            # Login sequence end
            await websocket.send(jsonify(payloads.cache_update(**self.cache)))

            while True:
                asyncio.sleep(0.1)
                data = decode(await websocket.recv())
                print(data)
                if data is None:
                    continue
                elif data.get('op') == 1 and data.get('d', {}).get('content'):
                    content = data['d']['content']
                    if content.startswith(self.command_prefix):
                        response = await self.execute(content, user)
                        if response is None:
                            pl = payloads.message_recieved(author=user.name, content=content)
                            for ws in user.room.sockets:
                                await ws.send(json(pl))
                    else:
                        pl = payloads.message_recieved(author=user.name, content=content)
                        for ws in user.room.sockets:
                            await ws.send(jsonify(pl))
                else:
                    continue

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
        print(f'Serving @ {self.host}:{self.port}')
        self.loop.run_forever()


def main():
    try:
        server = Server(loop)
        server.serve()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
