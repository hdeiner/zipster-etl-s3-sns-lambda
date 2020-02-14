### Rethinking ETL in a Serverless World

##### Concept
Right now, we use expensive tools such as Informatica to do ETL processing and ingestion of data.  Besides cost, there are issues such as lean wastes due to large batch size, quality, difficult testing, and so on.  So, here is an alternative to rethink the problem.  What if we built small serverless lambda functions (such as AWS Lambda), and coupled this with Simple Storage Service (AWS S3) and Simple Notification Service (AWS SNS) to transform and process input into loadable data for backend storage, along with error reporting?  This coukld make use of all of the advantages of Cloud Computing (only pay for what you use), as well as the advantages of Infrastructurre as Code (IaC).  Code could be written in whatever langue we want (I used Python here), tested locally, brought into AWS infrastructure using Terraform (allowing Contunuous Deployment using Git Pull Requests).  By the use of SNS, processing is as easy as creating an object in an designated S3 bucket, and monitoring using things like eMail and SMS integrated.

Here's a system level diagram is what this project looks like:

![architectural_diagram](assets/2020.02.11 zipster-s3-sns-lambda-etl.png)

##### Demo
###### Chapter 1 - look at our test input
![test_input](assets/test_input.png)

###### Chapter 2 - our etl_transform program
![etl_transform_1](assets/etl_transform_1.png)
![etl_transform_2](assets/etl_transform_2.png)
![etl_transform_3](assets/etl_transform_3.png)
![etl_transform_4](assets/etl_transform_4.png)

###### Chapter 3 - (manual for now) testing the etl_transform locally 
![etl_transform_local_test_1](assets/etl_transform_local_test_1.png)

![etl_transform_local_test_2](assets/etl_transform_local_test_2.png) 

###### Chapter 4 - our etl_load program
![etl_load_1](assets/etl_load_1.png)
![etl_load_2](assets/etl_load_2.png)

###### Chapter 5 - (manual for now) testing the etl_load locally (Docker used for MySQL database) 

Building the MySQL image (with local storage) in a version controlled way (all DDL and static data to a particular version created)

![step_2_dockerize_zipster-mysql_1](assets/step_2_dockerize_zipster-mysql_1.png) 

![step_2_dockerize_zipster-mysql_2](assets/step_2_dockerize_zipster-mysql_2.png) 

![step_2_dockerize_zipster-mysql_3](assets/step_2_dockerize_zipster-mysql_3.png) 

![step_2_dockerize_zipster-mysql_4](assets/step_2_dockerize_zipster-mysql_4.png) 

![step_2_dockerize_zipster-mysql_5](assets/step_2_dockerize_zipster-mysql_5.png) 

Start MySQL container from the image we just produced

![step_3_start_mysql_in_docker_composed_environment](assets/step_3_start_mysql_in_docker_composed_environment.png) 

Run etl_load

![step_4_local_test_sql_process](assets/step_4_local_test_sql_process.png) 

Cleanup local MySQL test environment

![step_5_destroy_mysql_docker_composed_environment](assets/step_5_destroy_mysql_docker_composed_environment.png) 

###### Chapter 6 - revealing the AWS infrastructure

![terraform_source_versions](assets/terraform_source_versions.png)

![terraform_source_provider](assets/terraform_source_provider.png)

![terraform_source_s3_buckets](assets/terraform_source_s3_buckets.png)

![terraform_source_sns_topics](assets/terraform_source_sns_topics.png)

![terraform_source_ec2_mysql_1](assets/terraform_source_ec2_mysql_1.png)

![terraform_source_ec2_mysql_2](assets/terraform_source_ec2_mysql_2.png)

![terraform_source_provision_mysql](assets/terraform_source_provision_mysql.png)

![terraform_source_lambda_etl_1](assets/terraform_source_lambda_etl_1.png)

![terraform_source_lambda_etl_2](assets/terraform_source_lambda_etl_2.png)

![terraform_source_lambda_etl_3](assets/terraform_source_lambda_etl_3.png)

![terraform_source_lambda_etl_4](assets/terraform_source_lambda_etl_4.png)

![terraform_source_lambda_etl_5](assets/terraform_source_lambda_etl_5.png)

![terraform_source_lambda_etl_6](assets/terraform_source_lambda_etl_6.png)

###### Chapter 8 - creating the AWS infrastructure

![terraform_create_1](assets/terraform_create_1.png) 

![terraform_create_2](assets/terraform_create_2.png) 

![terraform_create_3](assets/terraform_create_3.png) 

![terraform_create_4](assets/terraform_create_4.png) 

![terraform_create_5](assets/terraform_create_5.png) 

![terraform_create_6](assets/terraform_create_6.png) 

![terraform_create_7](assets/terraform_create_7.png) 

![terraform_create_8](assets/terraform_create_8.png)  

###### Chapter 11 - SNS subscription verifications

![sns_subscription_veification_1](assets/sns_subscription_veification_1.png) 

![sns_subscription_veification_2](assets/sns_subscription_veification_2.png) 

![sns_subscription_veification_3](assets/sns_subscription_veification_3.png) 

![sns_subscription_veification_4](assets/sns_subscription_veification_4.png) 

###### Chapter 10 - kick off an etl

![kick_off_etl](assets/kick_off_etl.png) 

###### Chapter 10 - verify on AWS Console and eMails

![sns_subscription_veification_1](assets/sns_subscription_veification_1.png) 

![sns_subscription_veification_2](assets/sns_subscription_veification_2.png) 

![sns_subscription_veification_3](assets/sns_subscription_veification_3.png) 

![sns_subscription_veification_4](assets/sns_subscription_veification_4.png) 

![aws_console_s3](assets/aws_console_s3.png) 

![aws_console_ec2](assets/aws_console_ec2.png) 

![aws_console_sns](assets/aws_console_sns.png) 

![aws_console_lambda_functions](assets/aws_console_lambda_functions.png) 

![aws_console_lambda_function_transform](assets/aws_console_lambda_function_transform.png) 

![aws_console_lambda_function_load](assets/aws_console_lambda_function_load.png) 

![aws_console_lambda_function_transform_log](assets/aws_console_lambda_function_transform_log.png) 

![aws_console_lambda_function_load_log](assets/aws_console_lambda_function_load_log.png) 

![verify_etl_using_mysql_workbench](assets/verify_etl_using_mysql_workbench.png) 

###### Chapter 11 - destroy the AWS infrastructure

![terraform_destroy_](assets/terraform_destroy_1.png)

![terraform_destroy_2](assets/terraform_destroy_2.png)

