import asyncio

success = "ok\n"
error = "error\nwrong command\n\n"
metrics = {}


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):

    def process_data(self, data):
        request = data.rstrip().split(' ')
        command = request[0]
        if command == 'get':
            return self.get(request)
        elif command == 'put':
            return self.put(request)
        else:
            return error

    def get(self, data):
        metric = data[1]
        response = success
        if metric == '*':
            for key, values in metrics.items():
                for value in values:
                    response = response + metric + ' ' + value[1] + ' ' + value[0] + '\n'
        else:
            if metric in metrics:
                for value in metrics[metric]:
                    response = response + metric + ' ' + value[1] + ' ' + value[0] + '\n'

        # print(response)
        return response + '\n'

    def put(self, data):
        metric = data[1]
        value = data[2]
        timestamp = data[3]
        if not metric in metrics:
            metrics[metric] = list()
        if not (timestamp, value) in metrics[metric]:
            metrics[metric].append((timestamp, value))
            metrics[metric].sort(key=lambda tup: tup[0])
        return success + '\n'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = self.process_data(data.decode('utf-8'))
        self.transport.write(response.encode('utf-8'))


# run_server("127.0.0.1", 10003)
