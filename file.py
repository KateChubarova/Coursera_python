import os
import tempfile
import uuid


class File:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(file_name):
            self.file = open(file_name, "w")
            self.file.close()

    def read(self):
        with open(self.file_name, "r") as f:
            return f.read()

    def write(self, text):
        with open(self.file_name, "w") as f:
            f.write(text)

    def __add__(self, other):
        sum_file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        sum_file = File(sum_file_name)
        sum_file.write(self.read() + other.read())
        return sum_file

    def __iter__(self):
        self._curr = 0
        with open(self.file_name, "r") as f:
            self._lines = f.readlines()
        return self

    def __next__(self):
        try:
            line = self._lines[self._curr]
            self._curr += 1
            return line
        except IndexError:
            raise StopIteration

    def __str__(self):
        return self.file_name
