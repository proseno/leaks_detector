import os
import sys
sys.path.append("..")
sys.path.append('generator')
import hashlib
import math
import subprocess
from generator.path import PathHandler
import csv
import json


class Log:
    def __init__(self):
        self.paths = PathHandler()
        self.log_path = os.path.join(self.paths.full_path, 'mysql.log')
        self.state_path = os.path.join(self.paths.tmp, 'state.json')
        self.md5 = None
        self.file_size = None
        self.lines_count = None

    def get_data(self, skip_init_read=True) -> list:
        self.load_state()
        if self.md5 is None or self.file_size is None or self.lines_count is None:
            result = self.read_new()
            if skip_init_read:
                result = []
        else:
            result = self.read_known()

        if len(result) >= 0:
            chunks = self.divide_in_chunks(result, 13)
            result = []
            for chunk in chunks:
                result.append('\n'.join(chunk))

        self.save_state()
        return result

    def read_new(self):
        with open(self.log_path, "r") as log_file:
            result = log_file.readlines()
        self.md5 = hashlib.md5(open(self.log_path, 'rb').read()).hexdigest()
        self.file_size = os.path.getsize(self.log_path)
        self.lines_count = len(result)

        return result

    def read_known(self):
        result = []
        new_md5 = hashlib.md5(open(self.log_path, 'rb').read()).hexdigest()
        if new_md5 != self.md5:
            new_size = os.path.getsize(self.log_path)

            if self.lines_count <= 0:
                return self.read_new()
            # TODO implement tail
            # f = subprocess.Popen(['tail', '-F', self.log_path, '-n', str(lines_to_select)], stdout=subprocess.PIPE,
            #                      stderr=subprocess.PIPE)
            # result = f.stdout.readlines()

            with open(self.log_path, "r") as log_file:
                log_lines = log_file.readlines()
                result = log_lines[self.lines_count:]

            self.file_size = new_size
            self.md5 = new_md5
            self.lines_count = len(log_lines)
        return result

    @staticmethod
    def divide_in_chunks(lines: list, n: int) -> list:
        return [lines[i * n:(i + 1) * n] for i in range((len(lines) + n - 1) // n)]

    def save_state(self):
        with open(self.state_path, 'w') as jsonfile:
            data = {
                'file_size': self.file_size,
                'md5': self.md5,
                'lines_count': self.lines_count
            }
            json.dump(data, jsonfile)

    def load_state(self):
        try:
            with open(self.state_path, newline='') as jsonfile:
                data = json.load(jsonfile)
                self.file_size = data['file_size']
                self.md5 = data['md5']
                self.lines_count = data['lines_count']
        except FileNotFoundError:
            pass
