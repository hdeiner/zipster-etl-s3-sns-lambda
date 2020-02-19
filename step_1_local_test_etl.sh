#!/usr/bin/env bash

cd src/main/python

pytest lambda_etl_transform/* --verbose

python3 lambda_etl_transform/etl-transform.py -i test.csv -o test.sql -e test.err

cd -