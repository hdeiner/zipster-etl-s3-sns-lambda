#!/usr/bin/env bash

figlet -w 160 -f standard "Destroy ETL Environment"

cd src/main/iac/terraform_etl

terraform destroy -auto-approve

cd -