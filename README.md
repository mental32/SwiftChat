# SwiftChat
## Python websocket chat server software.
<br>
SwiftChat is a python websocket chat server application.
It's inspired by other social media and chat applications such as:
Skype, Discord and WhatsApp. Its designed to be interfaced with websites.
<br>
## Server opcodes
code | description
-----|------------
0 | Message recieved
1 | Room state chage
<br>
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
<br>
### Room state change
```
{
	"avalible": true|false,
	"room": "general"
}
```
