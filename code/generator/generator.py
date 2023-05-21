import os
import adaptor
import logs
from faker import Faker
from datetime import datetime
import random

username = "root"
password = "magento2"
host = "mysql"
port = "3306"


def main():
    generator = Generator(
        adaptor.Mysql(host, username, password, port),
        logs.MysqlLogs(),
        Faker()
    )
    generator.generate_negative_case(100)


class Generator:
    def __init__(self, mysql_adaptor: adaptor.Mysql, mysql_logs: logs.MysqlLogs, faker: Faker):
        self.connection = mysql_adaptor
        self.logs_manager = mysql_logs
        self.faker = faker

    def generate_positive_case(self, count: int):
        for i in range(count):
            database_name = self.faker.word()
            self.connection.create_database(database_name)

            last_line = self.logs_manager.get_line_count('/var/www/html/var/mysql/logs/mysql.log')

            # TODO remove or archive dump
            self.connection.create_dump(database_name, self.logs_manager.dumps)

            now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self.logs_manager.create_train_log_from_line(last_line, 'positive/' + database_name + '_' + now + '.log')
            self.connection.drop_database(database_name)

        self.connection.disconnect()

    def generate_negative_case(self, count: int):
        lines = []
        files = os.listdir(self.logs_manager.log)
        for file in files:
            with open(os.path.join(self.logs_manager.log, file), 'r') as log:
                lines += log.readlines()

        file_max_lines = 13
        min = 0
        max = len(lines) - 1 - file_max_lines
        for i in range(count):
            start_line = random.randint(min, max)
            self.logs_manager.create_train_file(
                'negative/' + str(i) + '.log',
                lines[start_line:start_line + file_max_lines]
            )


main()
