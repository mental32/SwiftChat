##
#  -*- coding: utf-8 -*-
##
import asyncio
import io
import shlex
import sys
import websockets
from contextlib import suppress

from . import (utils, payloads)
from .room import Room
from .user import User

class Server:
	_instance = None
	def __init__(self, **kwargs):
		Server._instance = self

		self.loop = asyncio.get_event_loop()
		self.sockets = set()
		self.users = set()

		self.host = kwargs.get('host', 'localhost')
		self.port = kwargs.get('port', 8765)
		self.command_prefix = kwargs.get('command_prefix', '!')
		self.stdout = kwargs.get('stdout', sys.stdout)

		self.rooms = [Room(name='general')]

	@property
	def default_room(self):
		return self.rooms[0]

	def get_user(self, username, room=None):
		for user in self.users:
			if isinstance(room, Room) and user.room.id != room.id:
				continue

			if username == user.name:
				return user

	def cache_for(self, user):
		cache = {
			'rooms': tuple(room.bucket for room in self.rooms),
			'users': tuple(user.name for user in self.users),
		}

		cache['me'] = {'room': user.room.id}
		return cache

	def log(self, data):
		self.stdout.write('[%s] %s\n' %(utils.human_time(), data))

	async def execute(self, data):
		if data.startswith(self.command_prefix):
			op, *args = shlex.split(data)
			return 0
		return 1

	async def on_handler_error(self, error):
		self.log('Error! %s' %(error))

	async def handler(self, ws, path):
		try:
			user = User(ws)
			self.sockets.add(ws)
			self.users.add(user)
			self.log('Got connection from (%s, %s)' %(user.addr[:2]))

			# login sequence
			while user.name is None:
				await asyncio.sleep(0.1)

				data = utils.jdecode(await ws.recv())
				if isinstance(data, dict):
					if data.get('op') == 1 and data.get('d', {}).get('content'):
						user.name = data['d']['content']
						user.room = self.default_room
						await ws.send(utils.jencode(payloads.cache_update(**self.cache_for(user))))
						await user.room.send('%s has entered the room' %(user.name))
						self.log('(%s, %s) has logged in as "%s"' %(user.addr[0], user.addr[1], user.name))
				else:
					raise Exception

			# main sequence
			while True:
				await asyncio.sleep(0.1)

				data = utils.jdecode(await ws.recv())
				self.log('%s: %s' %(user, data))
				if not isinstance(data, dict) or data.get('op') != 1:
					raise Exception

				sts = (await self.execute(data['d']['content']))
				if sts == 1:
					await user.room.send(data)

		except Exception as error:
			await self.on_handler_error(error)

		finally:
			self.sockets.remove(ws)
			self.users.remove(user)

			with suppress(AttributeError):
				user.room.remove(user)

	def serve(self):
		self.stderr = io.StringIO('[%s] setting up server stderr.\n' %(utils.human_time()))
		sys.stderr = self.stderr

		self.log('Starting swiftchat server on %s:%s' %(self.host, self.port))
		self.loop.run_until_complete(websockets.serve(self.handler, self.host, self.port))
		self.loop.run_forever()