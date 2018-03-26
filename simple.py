##
#  -*- coding: utf-8 -*-
##
import swiftchat

server = swiftchat.Server()

@server.command
async def echo(serv, usr, *text):
	await usr.room.send(' '.join(text))

server.serve()
