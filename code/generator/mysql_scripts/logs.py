import tarfile
import os.path
import time
import shutil


class MysqlLogs:
    full_path = '/var/www/logs/'

    def __init__(self):
        self.full_path = os.path.abspath('/var/www/logs')
        self.train = os.path.abspath('/var/www/html/train')
        self.archive_folder = os.path.join(self.full_path, 'archive')

        folders = [self.full_path, self.train, self.archive_folder]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def cleanup_logs(self):
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

