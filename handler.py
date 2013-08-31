import logging

from neodym.exceptions import NotYetInitialized, UnregisteredMessage
from neodym.message import Message


class Handler(object):
    __all__ = dict()
    __map__ = dict()

    def __init__(self, unique_identifier):
        self.unique_identifier = unique_identifier

        self.logger = logging.getLogger('Handler-%s' % id(self))
        self.logger.debug('Initializing: %s' % self)

        if not self.__map__:
            raise NotYetInitialized

        if not self.unique_identifier in self.__map__:
            raise UnregisteredMessage


        if not self.unique_identifier in self.__all__:
            self.__all__[self.unique_identifier] = [self]
        else:
            self.__all__[self.unique_identifier].append(self)

    def __repr__(self):
        return "<Handler(%s)>" % self.unique_identifier

    def __call__(self, message, connection):
        self.logger.debug('Received call-back.')
        if not isinstance(message, Message):
            raise TypeError('must be of type neodym.message.Message')

        self.handle(message, connection)
        return self

    def handle(self, message, connection):
        """Overwrite this method in custom handler"""
        pass

    @classmethod
    def get_handlers(cls, message):
        if isinstance(message, Message):
            if message.unique_identifier in cls.__map__:
                return cls.__all__[message.unique_identifier]
