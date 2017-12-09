# SwiftChat
## Python websocket chat server software.
<br>bundled with a python CLI client

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
