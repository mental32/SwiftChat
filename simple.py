##
#  -*- coding: utf-8 -*-
##
import swiftchat

server = swiftchat.Server()
server.serve()


'''
			await ws.send(jencode({'op': 0, 'd': {'content': 'login as:'}}))
			while user.name is None:
				data = jdecode(await websocket.recv())
				if not isinstance(data, dict):
					continue

				elif data.get('op') == 1 and data.get('d', {}).get('content'):
					user.name = data['d']['content']
					await user.swap_rooms(self.default_room, silent_entry=True)
					await ws.send(jencode(payloads.cache_update(**self.cache_for(user))))
					await user.room.send(user.name+' has entered the room')

			while True:
				# await asyncio.sleep(0.1)
				data = jdecode(await ws.recv())
				if not isinstance(data, dict):
					continue
				else:
					pass

		except Exception as e:
			print(e)
		finally:
			self.sockets.remove(ws)
			user.room.disconnect(user)
'''
