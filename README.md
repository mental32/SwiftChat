# SwiftChat
## Python websocket chat server software.

SwiftChat is a python websocket chat server application, 
inspired by other
<br>social media and chat applications such as: Skype, Discord and WhatsApp.
<br>Its designed to be interfaced with websites meaning you can write a client 
<br>handler or use one of the example ones included.

## Server opcodes
code | description | client action
-----|-------------|--------------
0 | Message recieved | recieve only
1 | Message create   | send only
2 | Room state chage | recieve only
3 | Server shutdown  | recieve only
4 | cache update | recieve only

### Message recieved
The Message recieved payload will be sent when the server recieves a Message create payload.<br>The payload data will contain the authors name and the contents of the message.
```
{
	"op": 0,
	"d": {
		"author": "Jimothy",
		"content": "Hello world!"
	}
}
```

### Message create
The Message create payload will only be sent by the client.
<br>The payload data will only contain the message contents. 
```
{
	"op": 1,
	"d": {
		"content": "Message contents!"
	}
}
```

### Room state change
The Room state change payload will be sent once the availbility of the room changes.<br>
A room may change its availability if:
* The room gets manually closed
* The room gets locked
* The room gets deleted
* The client has been banned from the room
```
{
	"op": 2,
	"d": {
		"available": true|false,
		"room": "general"
	}
}
```


### Server shutdown
A server may manually be shutdown from the console or an external shutdown payload with the correct authorization key.<br>
Reguardless if a server is manually triggered to shutdown it will send out the Server shutdown payload to warn its clients
```
{
	"op": 3,
	"d": {
		"reason": "Maintenance, this field may be null"
	}
}
```


### Cache update
The server sends a cache update once a client logs in succesfully or when the client sends a special request for the cache update.
<br>The cache contains:
* rooms
* server command prefix
* host name
* application port
* amount of users connected
```
{
	"op": 4,
	"d": {
		"rooms": ,
		"command_prefix": "\",
		"host": "localhost",
		"port": 8765,
		"users": 5
	}
}
```
