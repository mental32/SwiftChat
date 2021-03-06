# Payloads
A payload will be sent from the server to the client whenever the server<br>
has to move data relating to the client about itself or the clients context.<br>

A payload will typically be sent as JSON data.<br>
Any data being sent to the server has to also be JSON encoded.<br>
## A Typical payload
Field | Type | Description
------|------|------------
op | Integer | opcode for the payload
d  | mixed (JSON Values) | event data

```
{
	"op": 1,
	"d": {
		"contents": "Huzzuh"
	}
}
```

## Payload opcodes
code | name             | client action
-----|------------------|--------------
0    | Message recieved | recieve only
1    | Message create   | send only
2    | Room state chage | recieve only
3    | Server shutdown  | recieve only
4    | cache update     | recieve only

# Types of payloads
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
		"rooms": {"room name": room_data, ...},
		"command_prefix": "!",
		"host": "localhost",
		"port": 8765,
		"users": 5
		"me": {"room": room_id}
	}
}
```
