= Neodym

Neodym is a thin message-bus wrapper around asyncore. It includes a client and
a server dispatcher, as well as an easily configurable message-bus. Json serves
as the designated transport syntax.


= Examples

This is a simple server:

    :::python
    import neodym
    import logging

    neodym.log_level = logging.DEBUG
    baseConfig = neodym.baseConfig()
    logging.basicConfig(**baseConfig)

    neodym.register('echo', ['cargo'])
    neodym.init()

    server = neodym.Server(('127.0.0.1', 42742))
    server.server_activate()

    class EchoHandler(neodym.handler.Handler):
        def handle(self, message, connection):
            cargo = message.get_attr('cargo')
            message.set_attr('cargo', str(cargo).upper())
            connection.put(message)


    echo_handler = EchoHandler('echo')
    server.serve_forever()

This is a simple client:

    :::python
    import neodym
    import logging
    import time

    neodym.log_level = logging.DEBUG
    baseConfig = neodym.baseConfig()
    logging.basicConfig(**baseConfig)

    neodym.register('echo', ['cargo'])
    neodym.init()

    client = neodym.Client('127.0.0.1', 42742)
    client.client_connect()

    connection = client.connection()

    message = neodym.message.Message('echo', ['foobar'])
    connection.put(message)
    client.update()

    time.sleep(0.1)

    client.update()
