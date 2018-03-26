##
#  -*- coding: utf-8 -*-
##
import time
from contextlib import suppress

from . import (utils, payloads)

class Room:
	def __init__(self, name):
		self.name = name
		self.id = utils.make_id()

		self.bucketable = ['created_at', 'id', 'name', 'users']
		self.created_at = int(time.time())

		self.password = None
		self.sockets = set()
		self.users = []

	@property
	def bucket(self):
		return {key: getattr(self, key) for key in self.bucketable}

	@property
	def locked(self):
		return (self.password is not None)

	async def send(self, message):
		pl = payloads.message_recieved(self.name, content=message)
		for ws in self.sockets:
			await ws.send(utils.jencode(pl))

	def add(self, user):
		self.sockets.add(user.ws)
		self.users.append(user.name)

	def remove(self, user):
		with suppress(KeyError):
			self.sockets.remove(user.ws)

		with suppress(KeyError):
			self.users.remove(user.name)
