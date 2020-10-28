import asyncio

success = "ok\n"
error = "error\nwrong command\n\n"
metrics = dict()


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


class Item:
    def __init__(self, value, timestamp):
        self.value = float(value)
        self.timestamp = int(timestamp)

    def __eq__(self, other):
        return self.timestamp == other.timestamp


class ClientServerProtocol(asyncio.Protocol):

    def check_request(self, request):
        command = request[0]
        if command == 'get':
            return len(request) == 2
        elif command == 'put':
            if len(request) != 4:
                return False
            try:
                float(request[2])
                int(request[3])
            except:
                return False
        else:
            return False
        return True

    def process_data(self, data):
        request = data.rstrip().split(' ')
        if not self.check_request(request):
            return error
        command = request[0]
        if command == 'get':
            return self.get(request)
        if command == 'put':
            return self.put(request)

    def get(self, data):
        metric = data[1]
        response = success
        if metric == '*':
            for key in metrics:
                for item in metrics[key]:
                    response = response + key + ' ' + str(item.value) + ' ' + str(item.timestamp) + '\n'
        else:
            if metric in metrics:
                for item in metrics[metric]:
                    response = response + metric + ' ' + str(item.value) + ' ' + str(item.timestamp) + '\n'
        return response + '\n'

    def put(self, data):
        metric = data[1]
        value = data[2]
        timestamp = data[3]
        item = Item(value, timestamp)
        if not metric in metrics:
            metrics[metric] = list()
        if not item in metrics[metric]:
            metrics[metric].append(item)
        else:
            _metric = metrics[metric]
            index = _metric.index(item)
            _metric[index] = item
            metrics[metric] = _metric
        return success + '\n'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = self.process_data(data.decode('utf-8'))
        self.transport.write(response.encode('utf-8'))


# run_server("127.0.0.1", 8181)
