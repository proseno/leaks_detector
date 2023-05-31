#!/bin/sh
# connect to server
#ssh ubuntu@89.207.132.170
# make dump
docker exec -i first_ai_mysql mysqldump -uroot -pmagento2 --all-databases > dump.sql

sleep 10000s
# download dump
#scp dump.sql ubuntu@89.207.132.170:/home/data
