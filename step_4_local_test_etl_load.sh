#!/usr/bin/env bash

cd src/main/python

python3 lambda_etl_load/etl-load.py -s test.sql -r localhost -u user -p password -d zipster

cd -