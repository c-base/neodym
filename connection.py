import asyncore
import logging
import Queue

from neodym.exceptions import MalformedMessage
from neodym.message import Message


class Connection(asyncore.dispatcher):
    __all__ = []
    __hash__ = ""
    __chunk__ = 8192
    __timeout__ = 30

    def __init__(self, sock, parent):
        asyncore.dispatcher.__init__(self, sock=sock)
        self.parent = parent

        self.logger = logging.getLogger('Connection')
        self.logger.info('Initializing: %s' % self)

        self.send_queue = Queue.Queue()
        self.recv_queue = Queue.Queue()

        self.handshaking = False
        Connection.__all__.append(self)

    def __del__(self):
        self.logger.debug('Vanishing!')

    def writable(self):
        return not self.send_queue.empty()

    def handle_read(self):
        self.logger.debug('Data incoming...')
        chunk = self.recv(self.__chunk__)
        if not chunk:
            self.handle_close()

        lines = chunk.replace('\r\n', '\n').split('\n')
        self.logger.debug('Received data: %s' % str(lines))

        for line in lines:
            if line:
                message = Message.unpack(line)
                if message:
                    self.recv_queue.put(message)
                else:
                    self.logger.debug('Can not unpack message: %s' % str(message))

    def handle_write(self):
        message = self.send_queue.get()
        self.logger.debug('Handling write: %s' % message)
        if isinstance(message, Message):
            self.send(message.pack())
        else:
            self.send(str(message) + '\r\n')

    def handle_close(self):
        self.logger.debug('Closing!')
        if self in self.__all__:
            self.__all__.remove(self)
        self.close()

    def put(self, message):
        self.logger.debug('Throwing message into send queue: %s' % message)
        if not isinstance(message, Message):
            raise MalformedMessage

        self.send_queue.put(message)

    def get(self):
        self.logger.debug('Polling receive queue for messages')
        if not self.recv_queue.empty():
            return self.recv_queue.get()

