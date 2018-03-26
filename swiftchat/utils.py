##
#  -*- coding: utf-8 -*-
##
import json
import time
import random
import datetime

def jencode(data):
	return json.dumps(data)


def jdecode(data):
	try:
		return json.loads(data)
	except json.decoder.JSONDecodeError:
		return None


def human_time():
	date = datetime.datetime.now()
	return ':'.join(str(item).zfill(2) for item in (date.hour, date.minute, date.second))


def make_id():
	return random.randint(1, 100000000)
