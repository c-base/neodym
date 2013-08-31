""""""
__author__ = "Brian Wiborg <baccenfutter@c-base.org"
__date__ = "2013/08/31"

import client
import server
import connection
import message
import exceptions
import logging

msg_map = message.RegisteredMessageDict(
    handshake=['msg_map_hash']
)

log_level = logging.INFO
log_format = '%(asctime)16s Neodym %(levelname)10s %(name)32s - %(message)s'

def baseConfig():
    return {
        'level': log_level,
        'format': log_format,
    }

def init():
    msg_map_hash = msg_map.hash()
    msg_map.__hash__ = msg_map_hash
    message.Message.__map__ = msg_map
    server.Server.__hash__ = msg_map_hash
    client.Client.__hash__ = msg_map_hash
    connection.Connection.__hash__ = msg_map_hash


def register(unique_identifier, attrs):
    msg_map[unique_identifier] = attrs


from client import Client
from server import Server
from message import Message
