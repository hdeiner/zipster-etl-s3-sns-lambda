#!/usr/bin/env bash

cd src/main/python

python3 sql_process.py -s test.sql -r localhost -u user -p password -d zipster

rm test.sql test.err

cd -