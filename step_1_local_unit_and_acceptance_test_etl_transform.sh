#!/usr/bin/env bash

figlet -w 160 -f small "Local Unit and Acceptance Test ETL Transform"

figlet -w 160 -f small "Unit Tests"
cd src/main/python
pytest lambda_etl_transform/* --verbose
cd -

figlet -w 160 -f small "Acceptance Tests"
cd src/test/python/lambda_etl_transform
behave -v features/etl-transform.feature
mv test.* ../lambda_etl_load/.
cd -