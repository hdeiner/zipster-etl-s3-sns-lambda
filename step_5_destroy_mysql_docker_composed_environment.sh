#!/usr/bin/env bash

figlet -w 160 -f standard "Destroy MySQL docker-composed Environment"

docker-compose -f docker-compose-mysql-and-mysql-data.yml down

sudo -S <<< "password" rm -rf mysql-data