def message_recieved(author, content):
	return {'op': 0, 'd': {'author': author, 'content': content}}


def room_state_change(avaliable, room):
	return {'op': 2, 'd': {'avaliable': avaliable, 'room': room}}


def server_shutdown(reason=None):
	return {'op': 3, 'd': {'reason': reason}}


def cache_update(**kwargs):
	return {'op': 4, 'd': {**kwargs}}
