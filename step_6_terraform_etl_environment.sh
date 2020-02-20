#!/usr/bin/env bash

figlet -w 160 -f standard "Terraform ETL Environment"

cd src/main/iac/terraform_etl

terraform init
terraform apply -auto-approve

echo `terraform output mysql_dns | grep -o '".*"' | cut -d '"' -f2` > .mysql_dns

cd -
