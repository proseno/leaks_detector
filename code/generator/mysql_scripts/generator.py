import mysql.connector
import subprocess
import os
import adaptor
import logs


username = "root"
password = "magento2"
host = "mysql"
port = "3306"


mysql_adaptor = adaptor.Mysql(host, username, password, port)
mysql_logs = logs.MysqlLogs()

full_path = os.path.abspath("/var/www/html/generator/sql_scripts/")
folders = {
    'neg': os.path.join(full_path, 'neg'),
    'pos': os.path.join(full_path, 'pos')
}
for folderType, path in folders.items():
    files_path = [os.path.join(path, x) for x in os.listdir(path)]
    mysql_logs.cleanup_logs()
    for file_path in files_path:
        with open(file_path, "r") as file:
            content = file.read()
            queries = content.strip().split(";")
        for sql in queries:
            if sql:
                result = mysql_adaptor.query(sql)
        mysql_logs.move_train_logs(folderType)
