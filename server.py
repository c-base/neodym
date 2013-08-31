"""neodym.server

This module contains all routines for the neodym server.
"""
__author__ = "Brian Wiborg <baccenfutter@c-base.org"
__date__ = "2013/08/31"

import asyncore
import logging
import socket
import time

from neodym.connection import Connection
from neodym.exceptions import NotYetInitialized


class Server(asyncore.dispatcher):
    """neodym.server.Server

    The server listens on an address and waits for connection-request from
    clients. If a connection-request is received, a new instance of
    neodym.connection.Connection is initialized and the client socket is passed
    along. The connection can be obtained by calling the connection method.
    """
    __hash__ = ""
    __max__ = 3

    def __init__(self, address):
        """
        :param address:     address-tuple in format of ('127.0.0.1', 0)
        """
        asyncore.dispatcher.__init__(self)

        self.logger = logging.getLogger('Server-%s' % id(self))
        self.logger.debug('Initializing: %s' % self)

        if not self.__hash__:
            raise NotYetInitialized

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()

        self.set_reuse_addr()

    def __del__(self):
        """neodym.server.Server.__del__

        Leave a note in the neodym logs if the server vanishes.
        """
        self.logger.debug('Vanishing!')

    def server_activate(self):
        """neodym.server.Server.server_activate

        Active the server, e.g. start listening.
        """
        self.logger.info('Binding on %s (max: %s)' % (self.address,
                                                       self.__max__))
        self.listen(self.__max__)

    def handle_accept(self):
        """asyncore.dispatcher.handle_accept
        """
        self.logger.info('Connection request incoming...')
        client_info = self.accept()
        if client_info:
            socket, port = client_info
            Connection(socket, self)

    def handle_close(self):
        """asyncore.dispatcher.handle_close"""
        self.logger.info('Closing.')
        self.close()

    def update(self):
        """neodym.server.Server.update

        Call asyncore.poll2 and then iterate over all connections and handle
        any given input.
        """
        asyncore.poll2()
        pass

        connections = [c for c in Connection.__all__]
        if connections:
            for c in connections:
                if not c.recv_queue.empty():
                    message = c.recv_queue.get()
                    self.logger.debug('Received message: %s' % message)

                    # perform handshake operation on new connections
                    if c.is_connected is False:
                        if message.unique_identifier == 'handshake':
                            self.logger.debug('Handling handshake request...')
                            if message.get_attr('msg_map_hash') == self.__hash__:
                                self.logger.info('Handshake: OK -> Connection-%s' % id(c))
                                c.is_connected = True
                                c.put(message)
                                c.handle_write()
                            else:
                                self.logger.info('Hash mismatch!')

                    # handle the message for all connected clients
                    elif c.is_connected is True:
                        # todo: handle message
                        c.logger.info(message)

                    else:
                        self.logger.debug('Internal server error!')
        else:
            time.sleep(0.1)

    def serve_forever(self):
        """neodym.server.Server.serve_forever

        Update the server in a continuous loop.
        """
        while True:
            self.update()
