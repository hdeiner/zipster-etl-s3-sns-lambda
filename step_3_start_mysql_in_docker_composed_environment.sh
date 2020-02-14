#!/usr/bin/env bash

figlet -w 160 -f standard "Start MySQL in docker-composed Environment"

sudo -S <<< "password" tar -xf mysql-data.tar.gz

docker-compose -f docker-compose-mysql-and-mysql-data.yml up -d

figlet -w 160 -f small "Wait for MySQL to Start"
while true ; do
  result=$(docker logs mysql 2>&1 | grep -c "Version: '5.7.28'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)")
  if [ $result != 0 ] ; then
    echo "MySQL has started"
    break
  fi
  sleep 5
done

