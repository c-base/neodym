"""neodym.client

This module contains all routines for the neodym client.
"""
__author__ = "Brian Wiborg <baccenfutter@c-base.org"
__date__ = "2013/08/31"

import asyncore
import logging
import socket

from neodym.connection import Connection
from neodym.message import Message


class Client(asyncore.dispatcher):
    """neodym.client.Client

    The client connects to a server and tries to establish a connection by
    performing a handshaking procedure. If the handshake completes
    successfully, the client can send messages to the server.
    """
    __hash__ = ""

    def __init__(self, host, port):
        """
        :param host:    hostname or ip of server as string
        :param port:    TCP port as integer
        """
        self.host = host
        self.port = port
        asyncore.dispatcher.__init__(self)

        self.logger = logging.getLogger('Client-%s' % id(self))
        self.logger.debug('Initializing: %s' % self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__connection = None

    def handle_connect(self):
        """asyncore.handle_connect
        """
        self.logger.info('Connected to server, establishing connection...')
        self.__connection = Connection(self.socket, self)

    def handle_close(self):
        """asyncore.handle_close
        """
        self.logger.info('Closing.')
        Connection.__all__ = set()

    def client_connect(self):
        """neodym.client.Client.client_connect

        Connect to server.
        """
        self.connect((self.host, self.port))
        pass
        self.update()
        pass

    def update(self):
        """neodym.client.Client.update

        Poll asyncore, pass and return.
        """
        asyncore.poll2()
        pass
        return

    def connection(self):
        """neodym.client.Client.connection

        Obtain an established connection from the client by performing the
        handshaking procedure with the server.

        :returns neodym.connection.Connection:  the connection instance
        """
        handshake = Message('handshake', [self.__hash__])
        self.__connection.put(handshake)

        while self.__connection.recv_queue.empty():
            self.update()

        message = self.__connection.recv_queue.get()
        if not message:
            self.logger.info('Timeout reached!')
            self.close()
        elif message.unique_identifier == 'handshake':
            self.logger.info('Connection established.')
            return self.__connection
