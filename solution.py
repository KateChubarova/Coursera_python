import socket
import time

encoding = "utf-8"
success = "ok\n"


class ClientError(Exception):
    pass


class Client:

    def __init__(self, address, port, timeout=0):
        self.address = address
        self.port = port
        self.timeout = timeout

    def get_data(self, request):
        with socket.create_connection((self.address, self.port), self.timeout) as s:
            s.sendall(request.encode(encoding))
            response = s.recv(1024).decode(encoding)
            if not response.startswith(success):
                raise ClientError(response)
            return response

    def check_metric_valid(self, metric):
        if len(metric) != 3: return False
        try:
            float(metric[1])
            int(metric[2])
        except ValueError:
            return False

        return True

    def put(self, metric, value, timestamp=-1):
        if timestamp < 0:
            timestamp = int(time.time())
        request = 'put ' + metric + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        self.get_data(request)

    def get(self, metric):
        request = 'get ' + metric + '\n'
        response = self.get_data(request)
        metrics_dict = dict()
        metrics = response.split('\n')
        for l in metrics[1:-2]:
            metric = l.split(' ')
            if not self.check_metric_valid(response):
                raise ClientError(response)
            res_key = metric[0]
            res_val = float(metric[1])
            res_ts = int(metric[2])
            if not res_key in metrics_dict:
                metrics_dict[res_key] = list()
            metrics_dict[res_key].append((res_ts, res_val))
            metrics_dict[res_key].sort(key=lambda tup: tup[0])
        return metrics_dict
