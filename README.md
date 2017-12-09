# SwiftChat
## Python websocket chat server software.

SwiftChat is a python websocket chat server application, 
inspired by other<br>social media and chat applications such as:
Skype, Discord and WhatsApp. Its designed to be interfaced with websites.

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
	"avalible": true|false,
	"room": "general"
}
```
