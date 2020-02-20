#!/usr/bin/env bash

figlet -w 160 -f standard "AWS Integration Test ETL Transform and Load"

cd src/test/python/aws_etl_transform_and_load_integration_test
behave -v features/etl-transform-and-load.feature
rm -rf awsintegrationtest awsintegrationtest_errors
cd -