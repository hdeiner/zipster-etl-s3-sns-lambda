#!/usr/bin/env bash

figlet -w 160 -f standard "Terraform ETL Environment"

#cd src/main/python
#zip -r  ../iac/terraform_etl/sql_process.zip sql_process.py pymysql
#cd -

cd src/main/iac/terraform_etl

terraform init
terraform apply -auto-approve

cd -

#figlet -w 160 -f small "Provision MySQL in AWS"

#bolt command run '/home/ubuntu/provision_mysql.sh' --targets $(<.mysql_dns) --user 'ubuntu' --no-host-key-check | tee /dev/null