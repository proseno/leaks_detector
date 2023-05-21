import mysql.connector
import subprocess
import os
from datetime import datetime


class Mysql:
    def __init__(self, host: str, username: str, password: str, port: str):

        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = self.connect()

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            port=self.port
        )

    def disconnect(self):
        self.client.disconnect()
    
    def create_database(self, database: str):
        cursor = self.client.cursor()
        cursor.execute("CREATE DATABASE `" + database + "`")

    def drop_database(self, database: str):
        cursor = self.client.cursor()
        cursor.execute("DROP DATABASE `" + database + "`")

    def query(self, sql: str):
        # todo check what is going on here
        cursor = self.client.cursor()
        cursor.execute(sql)
        result = []
        for i in cursor:
            result += i
        return result

    def create_dump(self, database: str, path: str):
        if not os.path.exists(path):
            os.mkdir(path)

        now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = os.path.join(path, database + "_" + now + '.sql')
        command = ["mysqldump", "-h", self.host, "-u", self.username, "-p" + self.password, database]
        with open(file, 'w') as file:
            subprocess.call(command, stdout=file)
