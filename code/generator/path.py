import os


class PathHandler:
    def __init__(self):
        self.root = os.path.abspath('/var/www/html/')
        self.full_path = os.path.join(self.root, 'var/mysql/logs')
        self.train = os.path.join(self.root, 'var/mysql/train')
        self.train_positive = os.path.join(self.root, 'var/mysql/train/positive')
        self.train_negative = os.path.join(self.root, 'var/mysql/train/negative')
        self.train_merged = os.path.join(self.root, 'var/mysql/train/merged')
        self.archive_folder = os.path.join(self.full_path, 'archive')
        self.dumps = os.path.join(self.root, 'var/mysql/dumps/')
        self.log = os.path.join(self.root, 'var/log')

        for folder in vars(self).values():
            if not os.path.exists(folder):
                os.makedirs(folder)

