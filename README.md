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
1 | Message created  | send only
2 | Room state chage | recieve only

### Message recieved
The Message recieved payload will be sent when the server recieves a Message created payload.<br>The Message recieved payload data will contain the authors name and the contents of the message.
```
{
	"op": 0,
	"d": {
		"author": "Jimothy",
		"contents": "Hello world!"
	}
}
```

### Room state change
```
{
	"op": 2,
	"d": {
		"avalible": true|false,
		"room": "general"
	}
}
```
