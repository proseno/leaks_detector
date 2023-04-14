import mysql.connector
import subprocess
import os

username = "root"
password = "magento2"
host = "mysql"
port = "3307"
path_to_dumps = "/var/www/dumps/"


def create_dump(database: str):
    if not os.path.exists(path_to_dumps):
        os.makedirs(path_to_dumps)
    file = path_to_dumps + database + '.sql'
    command = ["mysqldump", "-h", host, "-u", username, "-p" + password, database]
    with open(file, 'w') as file:
        subprocess.call(command, stdout=file)


class Mysql:
    def __init__(self, host: str, username: str, password: str, port: str):
        self.client = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            port=port
        )

    def disconnect(self):
        self.client.disconnect()
    
    def create_database(self, database: str):
        cursor = self.client.cursor()
        cursor.execute("CREATE DATABASE " + database)

    def query(self, sql: str):
        cursor = self.client.cursor()
        cursor.execute(sql)
        result = []
        for i in cursor:
            result += i
        return result
