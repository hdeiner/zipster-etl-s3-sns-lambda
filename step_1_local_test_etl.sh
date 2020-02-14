#!/usr/bin/env bash

cd src/main/python

python3 lambda_etl_transform/etl-transform.py -i test.csv -o test.sql -e test.err

cd -