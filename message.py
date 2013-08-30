import logging
import UserDict
import hashlib
import json

from neodym.exceptions import AlreadyInitialized, MalformedMessage, UnregisteredMessage


class RegisteredMessageDict(UserDict.IterableUserDict):
    __hash__ = ""

    def __init__(self, *args, **kwargs):
        self.data = {}

        self.logger = logging.getLogger('RegisteredMessageDict')
        self.logger.info('Initializing: %s' % self)

        UserDict.IterableUserDict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        if self.__hash__:
            raise AlreadyInitialized

        if not isinstance(key, str) or not isinstance(value, list):
            raise ValueError('Key must be a string and value must be a list!')
        self.data[key] = value

    def __delitem__(self, key):
        if self.__hash__:
            raise AlreadyInitialized

    def hash(self):
        msg_map = [(k, self.data[k]) for k in sorted(self.data)]
        return hashlib.md5(str(msg_map)).hexdigest()


class Message(object):
    __map__ = dict()    # dictionary of all registered messages

    def __init__(self, unique_identifier, attrs):
        self.unique_identifier = unique_identifier
        self.attrs = attrs

        self.logger = logging.getLogger('Message-%s' % id(self))
        self.logger.debug('Initializing: %s' % self)

        if not (
            isinstance(self.unique_identifier, str) and
            isinstance(self.attrs, list) and
            len(self.attrs) == len(self.__map__[self.unique_identifier])
        ):
            raise MalformedMessage

        if not self.unique_identifier in self.__map__:
            raise UnregisteredMessage

    def __repr__(self):
        return "<Neodym.Message(%s)>" % self.pack()[:-2]

    def get_attr(self, attr):
        if attr in self.__map__[self.unique_identifier]:
            index = self.__map__[self.unique_identifier].index(attr)
            return self.attrs[index]
        else:
            self.logger.debug('Referencing illegal attribute: %s' % str(attr))

    def set_attr(self, attr, value):
        if attr in self.__map__[self.unique_identifier]:
            index = self.__map__[self.unique_identifier].index(attr)
            self.attrs[index] = value
        else:
            self.logger.debug('Trying to set unknown attribute: %s' % str(attr))

    def get_attrs(self):
        return zip(self.__map__[self.unique_identifier], self.attrs)

    def set_attrs(self, attrs):
        if not isinstance(attrs, dict):
            raise TypeError('Attributes must be passed as dictionary!')

        for attr, value in attrs.items():
            self.set_attr(attr, value)

    def pack(self):
        return json.dumps({self.unique_identifier: self.attrs}) + '\r\n'

    @classmethod
    def unpack(cls, line):
        try:
            message = json.loads(line.strip())
            unique_identifier, attrs = message.items()[0]
            return Message(str(unique_identifier), attrs)
        except:
            logging.debug('Error while unpacking line: %s' % line)

