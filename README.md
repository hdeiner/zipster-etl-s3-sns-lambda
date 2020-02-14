### Rethinking ETL in a Serverless World

##### Concept
Right now, we use expensive tools such as Informatica to do ETL processing and ingestion of data.  Besides cost, there are issues such as lean wastes due to large batch size, quality, difficult testing, and so on.  So, here is an alternative to rethink the problem.  What if we built small serverless lambda functions (such as AWS Lambda), and coupled this with Simple Storage Service (AWS S3) and Simple Notification Service (AWS SNS) to transform and process input into loadable data for backend storage, along with error reporting?  This coukld make use of all of the advantages of Cloud Computing (only pay for what you use), as well as the advantages of Infrastructurre as Code (IaC).  Code could be written in whatever langue we want (I used Python here), tested locally, brought into AWS infrastructure using Terraform (allowing Contunuous Deployment using Git Pull Requests).  By the use of SNS, processing is as easy as creating an object in an designated S3 bucket, and monitoring using things like eMail and SMS integrated.

Here's a system level diagram is what this project looks like:

![architectural_diagram](assets/2020.02.11 zipster-s3-sns-lambda-etl.png)

##### Demo
###### Step 1 - look at our test input
![test_input](assets/test_input.png)

###### Step 2 - our etl_transform program
![etl_transform_1](assets/etl_transform_1.png)
![etl_transform_2](assets/etl_transform_2.png)
![etl_transform_3](assets/etl_transform_3.png)
![etl_transform_4](assets/etl_transform_4.png)

###### Step 3 - (manual for now) testing the etl_transform locally 
![etl_transform_local_test_1](assets/etl_transform_local_test_1.png)

![etl_transform_local_test_2](assets/etl_transform_local_test_2.png) 

###### Step 4 - create the infrastructure
![terraform_init](assets/terraform_init.png)

![terraform_apply](assets/terraform_apply.png)

###### Step 5 - kick off an etl
![kick_off_etl](assets/kick_off_etl.png) 

###### Step 6 - verify on AWS Console and eMails
![aws_verify_1](assets/aws_verification_1.png) 

![aws_verify_2](assets/aws_verification_2.png) 

![aws_verify_3](assets/aws_verification_3.png) 

![aws_verify_4](assets/aws_verification_4.png) 

![aws_verify_5](assets/aws_verification_5.png) 

![aws_verify_6](assets/aws_verification_6.png) 

###### Step 7 - destroy the infrastructure
![terraform_destroy](assets/terraform_destroy.png)

