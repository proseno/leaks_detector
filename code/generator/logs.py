import tarfile
import os.path
import time
import shutil


class MysqlLogs:
    def __init__(self):
        self.root = os.path.abspath('/var/www/html/')
        self.full_path = os.path.join(self.root, 'var/mysql/logs')
        self.train = os.path.join(self.root, 'var/mysql/train')
        self.train_positive = os.path.join(self.root, 'var/mysql/train/positive')
        self.train_negative = os.path.join(self.root, 'var/mysql/train/negative')
        self.archive_folder = os.path.join(self.full_path, 'archive')
        self.dumps = os.path.join(self.root, 'var/mysql/dumps/')
        self.log = os.path.join(self.root, 'var/log')

        folders = [self.full_path, self.train, self.train_positive, self.train_negative, self.archive_folder]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def cleanup_logs(self):
        # deprecated
        files_path = os.listdir(self.full_path)
        for file_name in files_path:
            file_path = os.path.join(self.full_path, file_name)
            if os.path.isfile(file_path):
                destination = os.path.join(self.archive_folder, file_name) + str(time.time()) + '.tar.gz'
                with tarfile.open(destination, "w:gz") as tar:
                    tar.add(file_path, arcname=os.path.basename(file_path))
                if os.path.exists(file_path):
                    os.remove(file_path)
                    if not os.path.exists(file_path):
                        open(file_path, "w").close()

    def get_logs(self):
        log_file = os.path.join(self.full_path, 'mysql.log')
        with open(log_file, 'r') as log:
            content = log.read()
        return content

    def move_train_logs(self, destination: str):
        log_file = os.path.join(self.full_path, 'mysql.log')
        destination_file = os.path.join(self.train, destination + '/mysql.log')
        shutil.move(log_file, destination_file)

    @staticmethod
    def get_line_count(filename):
        count = 0
        with open(filename, 'r') as file:
            for _ in file:
                count += 1
        return count

    def create_train_log_from_line(self, line_number: int, destination: str):
        log_file = os.path.join(self.full_path, 'mysql.log')
        destination_file = os.path.join(self.train, destination)
        with open(log_file, 'r') as file:
            with open(destination_file, 'w') as destination_file:
                for i, line in enumerate(file):
                    if i >= line_number:
                        destination_file.write(line)

    def create_train_file(self, destination: str, lines: list):
        destination_file = os.path.join(self.train, destination)
        with open(destination_file, 'w') as destination_file:
            for line in lines:
                destination_file.write(line)
