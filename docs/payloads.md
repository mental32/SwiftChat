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
