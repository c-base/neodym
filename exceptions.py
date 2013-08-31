""""""
__author__ = "Brian Wiborg <baccenfutter@c-base.org"
__date__ = "2013/08/31"

class NeodymException(Exception):
    pass

class NotYetInitialized(NeodymException):
    """Neodym is not yet initialized"""
    def __init__(self):
        NeodymException.__init__(self, self.__doc__)

class AlreadyInitialized(NeodymException):
    """Neodym is already initialized!"""
    def __init__(self):
        NeodymException.__init__(self, self.__doc__)

### Messages ###
class NeodymMessageException(NeodymException):
    pass

class UnregisteredMessage(NeodymMessageException):
    """All transport messages need to be registered before initializing Neodym."""
    def __init__(self):
        NeodymMessageException.__init__(self, self.__doc__)

class MalformedMessage(NeodymMessageException):
    """The message is malformed or invalid"""
    def __init__(self):
        NeodymMessageException.__init__(self, self.__doc__)
