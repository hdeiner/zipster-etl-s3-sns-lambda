#!/usr/bin/env bash

figlet -w 160 -f standard "Dockerize zipster-mysql"

figlet -w 160 -f small "Create MySQL Container"
docker stop mysql
docker rm mysql
docker rmi -f howarddeiner/zipster-mysql
docker build src/main/iac/docker-mysql/ -t howarddeiner/zipster-mysql

figlet -w 160 -f small "Bring Up MySQL Container"
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

figlet -w 160 -f small "Ready MySQL for FlyWay"
echo "CREATE USER 'FLYWAY' IDENTIFIED BY 'FLWAY';" | mysql -h 127.0.0.1 -P 3306 -u root --password=password  zipster > /dev/null

figlet -w 160 -f small "Load Initial Data Into Database"
./flyway-4.2.0/flyway info
./flyway-4.2.0/flyway -target=2_1 migrate
./flyway-4.2.0/flyway info

figlet -w 160 -f standard "Create zipster-mysql Image"

figlet -w 160 -f small "Commit and Push the Zipster MySQL Container to Store the Image"
docker exec mysql mysqladmin --password=password shutdown
sleep 15
docker rmi -f howarddeiner/zipster-mysql
docker stop mysql
docker commit mysql howarddeiner/zipster-mysql
docker login
docker push howarddeiner/zipster-mysql

figlet -w 160 -f small "Serialize the mysql-data"
sudo -S <<< "password"  tar -czf mysql-data.tar.gz mysql-data

figlet -w 160 -f small "Bring Down MySQL Continer"
docker-compose -f docker-compose-mysql-and-mysql-data.yml down
sudo -S <<< "password" rm -rf .mysql-data
