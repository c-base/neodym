import asyncore
import logging
import socket

from neodym.connection import Connection
from neodym.message import Message


class Client(asyncore.dispatcher):
    __hash__ = ""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        asyncore.dispatcher.__init__(self)

        self.logger = logging.getLogger('Client')
        self.logger.info('Initializing: %s' % self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection = None

    def handle_connect(self):
        self.logger.info('Connected to server, establishing connection...')
        self.connection = Connection(self.socket, self)

    def handle_close(self):
        self.logger.info('Closing.')
        Connection.__all__ = set()
        self.close()

    def client_connect(self):
        self.connect((self.host, self.port))
        pass
        self.update()
        pass

    def update(self):
        asyncore.poll2()
        pass
        return

    def session(self):
        handshake = Message('handshake', [self.__hash__])
        self.connection.put(handshake)

        while self.connection.recv_queue.empty():
            self.update()

        message = self.connection.recv_queue.get()
        if not message:
            self.logger.info('Timeout reached!')
            self.handle_close()
            return
        print message
