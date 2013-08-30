import asyncore
import logging
import socket
import time


from neodym.connection import Connection
from neodym.exceptions import NotYetInitialized

class Server(asyncore.dispatcher):
    __hash__ = ""
    __max__ = 3

    def __init__(self, address):
        asyncore.dispatcher.__init__(self)

        self.logger = logging.getLogger('Server')
        self.logger.info('Initializing: %s' % self)

        if not self.__hash__:
            raise NotYetInitialized

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()

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
        for c in Connection.__all__:
            if not c.recv_queue.empty():
                message = c.recv_queue.get()
                self.logger.debug('Received message: %s' % message)
                if message.unique_identifier == 'handshake':
                    self.logger.debug('Handling handshake request...')
                    if message.get_attr('msg_map_hash') == self.__hash__:
                        self.logger.debug('Handshake: OK')
                        c.put(message)
                    else:
                        self.logger.debug('Hash mismatch!')
            else:
                self.logger.debug('Empty queue...')

