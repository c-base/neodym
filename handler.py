import logging

import exceptions
from message import Message


class Handler(object):
    __all__ = dict()
    __messages__ = dict()

    def __init__(self, unique_identifier):
        self.unique_identifier = unique_identifier

        self.logger = logging.getLogger('Handler')
        self.logger.debug('Initializing: %s' % self)

        if not self.__messages__:
            raise exceptions.NotYetInitialized

    def __repr__(self):
        return "<Handler(%s)>" % self.unique_identifier
