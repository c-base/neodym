import asyncore
import logging
import socket

from neodym.connection import Connection
from neodym.exceptions import NotYetInitialized


class Server(asyncore.dispatcher):
    __hash__ = ""
    __max__ = 3

    def __init__(self, address):
        asyncore.dispatcher.__init__(self)

        self.logger = logging.getLogger('Server-%s' % id(self))
        self.logger.info('Initializing: %s' % self)

        if not self.__hash__:
            raise NotYetInitialized

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()

        self.set_reuse_addr()

    def __del__(self):
        self.logger.debug('Vanishing!')

    def server_activate(self):
        self.logger.debug('Binding on %s (max: %s)' % (self.address,
                                                       self.__max__))
        self.listen(self.__max__)

    def handle_accept(self):
        self.logger.debug('Incoming connection request...')
        client_info = self.accept()
        if client_info:
            socket, port = client_info
            Connection(socket, self)

    def handle_close(self):
        self.logger.info('Closing.')
        self.close()

    def update(self):
        asyncore.poll2()
        pass

        for c in [c for c in Connection.__all__ if not c.is_connected]:
            if not c.recv_queue.empty():
                message = c.recv_queue.get()
                self.logger.debug('Received message: %s' % message)

                # perform handshake operation on new connections
                if c.is_connected is False:
                    if message.unique_identifier == 'handshake':
                        self.logger.debug('Handling handshake request...')
                        if message.get_attr('msg_map_hash') == self.__hash__:
                            self.logger.debug('Handshake: OK')
                            c.is_connected = True
                            c.put(message)
                            c.handle_write()
                        else:
                            self.logger.debug('Hash mismatch!')

                # handle the message for all connected clients
                elif c.is_connected is True:
                    # todo: handle message
                    self.logger.info(message)

                else:
                    self.logger.debug('Internal server error!')

    def serve_forever(self):
        while True:
            self.update()
