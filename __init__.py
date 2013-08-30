import client
import server
import connection
import message
import exceptions
import logging

msg_map = message.RegisteredMessageDict(
    handshake=['msg_map_hash']
)

baseConfig = {
    'level': logging.INFO,
    'format': '%(asctime)16s %(name)24s %(message)s'
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


def Message(*args, **kwargs):
    return message.Message(*args, **kwargs)
