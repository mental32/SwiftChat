##
#  -*- coding: utf-8 -*-
##
import signal

from . import server
from .errors import *
from .server import Server

signal.signal(signal.SIGINT, signal.SIG_DFL)

__version__ = '0.1.0'
__author__ = 'mental'
