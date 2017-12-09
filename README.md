# SwiftChat
## Python websocket chat server software.

SwiftChat is a python websocket chat server application, 
inspired by other
<br>social media and chat applications such as: Skype, Discord and WhatsApp.
<br>Its designed to be interfaced with websites meaning you can write a client 
<br>handler or use one of the example ones included.

## Server opcodes
code | description
-----|------------
0 | Message recieved
1 | Room state chage

### Message recieved
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
	"op": 1,
	"d": {
		"avalible": true|false,
		"room": "general"
	}
}
```
