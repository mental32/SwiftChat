# SwiftChat
## Python websocket chat server software.

SwiftChat is a python websocket chat server application, 
inspired by other
<br>social media and chat applications such as: Skype, Discord and WhatsApp.
<br>Its designed to be interfaced with websites meaning you can write a client 
<br>handler or use one of the example ones included.

## A Typical payload
Field | Type | Description
------|------|------------
op | Integer | opcode for the payload
d | mixed(JSON Values) | event data 

## Server opcodes
code | description | client action
-----|-------------|--------------
0 | Message recieved | recieve only
1 | Message create   | send only
2 | Room state chage | recieve only
3 | Server shutdown  | recieve only

### Message recieved
The Message recieved payload will be sent when the server recieves a Message create payload.<br>The payload data will contain the authors name and the contents of the message.
```
{
	"op": 0,
	"d": {
		"author": "Jimothy",
		"contents": "Hello world!"
	}
}
```

### Message create
The Message create payload will only be sent by the client.
<br>The payload data will only contain the message contents. 
```
{
	"op": 0,
	"d": {
		"content": "Message contents!"
	}
}
```

### Room state change
The Room state change payload will 
```
{
	"op": 2,
	"d": {
		"avalible": true|false,
		"room": "general"
	}
}
```
