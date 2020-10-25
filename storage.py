import os
import tempfile
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--value")
parser.add_argument("--key")
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def read():
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as f:
        raw_data = f.read()
        if raw_data:
            return json.loads(raw_data)

        return {}


_dict = read()
if args.value:
    with open(storage_path, 'w') as w:
        if args.key in _dict.keys():
            _list = _dict[args.key]
            _list.append(args.value)
            _dict[args.key] = _list
        else:
            _dict[args.key] = [args.value]
        json.dump(_dict, w)

else:
    if args.key in _dict.keys():
        print(', '.join(map(str, _dict[args.key])))
    else:
        print(None)
