##
#  -*- coding: utf-8 -*-
##
import time

from .errors import AuthenticationError
from .room import Room


class User:
	def __init__(self, ws, **kwargs):
		self.ws = ws
		self.addr = ws.remote_address

		self.connected_at = int(time.time())
		self.bucketable = ['connected_at', 'name']

		self.name = kwargs.get('name', None)
		self._room = kwargs.get('room', None)

	def __str__(self):
		return str(self.name)

	def __repr__(self):
		return 'User(name="%s", ip="%s")' %(self.name, self.addr[0])

	@property
	def bucket(self):
		return {key: getattr(self, key) for key in self.bucketable}

	@property
	def room(self):
		return self._room

	@room.setter
	def room(self, new_room):
		if new_room is not None:
			if self.room:
				self.room.remove(self)

			self._room = new_room
			new_room.add(self)

	async def swap_rooms(self, new_room, **kwargs):
		if isinstance(new_room, Room):
			if new_room.locked and new_room.password != kwargs.get('password'):
				raise AuthenticationError

			if self.room:
				await self.room.disconnect(self)
				if not kwargs.get('silent_exit', False):
					await self.room.send('%s has left the room.' %(self.name))

				self.room = new_room
				new_room.add(self)
