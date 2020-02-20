#!/usr/bin/env bash

figlet -w 160 -f small "Local Integration Test ETL Load"

figlet -w 160 -f small "Integration Tests"
cd src/test/python/lambda_etl_load
behave -v features/etl-load-local.feature
rm test.*
cd -