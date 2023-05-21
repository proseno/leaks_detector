import os
import adaptor
import logs
from faker import Faker
from datetime import datetime
import random
import path
import csv

username = "root"
password = "magento2"
host = "mysql"
port = "3306"


def main():
    generator = Generator(
        adaptor.Mysql(host, username, password, port),
        logs.MysqlLogs(),
        Faker(),
        path.PathHandler()
    )
    generator.convert_to_csv()


class Generator:
    def __init__(
            self,
            mysql_adaptor: adaptor.Mysql,
            mysql_logs: logs.MysqlLogs,
            faker: Faker,
            path_handler: path.PathHandler
    ):
        self.connection = mysql_adaptor
        self.logs_manager = mysql_logs
        self.faker = faker
        self.path_handler = path_handler

    def generate_positive_case(self, count: int):
        for i in range(count):
            database_name = self.faker.word()
            self.connection.create_database(database_name)

            last_line = self.logs_manager.get_line_count('/var/www/html/var/mysql/logs/mysql.log')

            # TODO remove or archive dump
            self.connection.create_dump(database_name, self.path_handler.dumps)

            now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self.logs_manager.create_train_log_from_line(last_line, 'positive/' + database_name + '_' + now + '.log')
            self.connection.drop_database(database_name)

        self.connection.disconnect()

    def generate_negative_case(self, count: int):
        lines = []
        files = os.listdir(self.path_handler.log)
        for file in files:
            with open(os.path.join(self.path_handler.log, file), 'r') as log:
                lines += log.readlines()

        file_max_lines = 13
        min = 0
        max = len(lines) - 1 - file_max_lines
        # TODO add continuous selection because random can select same line
        for i in range(count):
            start_line = random.randint(min, max)
            self.logs_manager.create_train_file(
                'negative/' + str(i) + '.log',
                lines[start_line:start_line + file_max_lines]
            )

    def convert_to_csv(self):
        positive_files = self.merge_array(self.path_handler.train_positive, 1)
        negative_files = self.merge_array(self.path_handler.train_negative, 0)
        data = positive_files + negative_files

        with open(os.path.join(self.path_handler.train_merged, 'merged_logs.csv'), 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['target', 'text'])
            for row in data:
                csv_writer.writerow([row['target'], row['text']])

    def merge_array(self, path_to_files: str, target: int):
        result = []
        files = os.listdir(path_to_files)
        for file in files:
            with open(os.path.join(path_to_files, file), 'r') as log:
                lines = log.readlines()
            result += [{"text": ' '.join(lines), "target": target}]

        return result


# main()
