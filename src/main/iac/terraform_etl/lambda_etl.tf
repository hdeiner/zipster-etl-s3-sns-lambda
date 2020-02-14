data "archive_file" "zipit_lambda_etl_transform" {
  type        = "zip"
  source_dir  = "../../python/lambda_etl_transform/"
  output_path = "lambda_etl_transform.zip"
}

data "archive_file" "zipit_lambda_etl_load" {
  type        = "zip"
  source_dir  = "../../python/lambda_etl_load/"
  output_path = "lambda_etl_load.zip"
}

resource "aws_lambda_function" "zipster-etl-s3-sns-lambda-transform" {
  role             = aws_iam_role.zipster-etl-s3-sns-lambda-transform-role.arn
  handler          = "etl-transform.lambda_handler"
  runtime          = "python3.6"
  filename         = data.archive_file.zipit_lambda_etl_transform.output_path
  source_code_hash = data.archive_file.zipit_lambda_etl_transform.output_base64sha256
  function_name    = "zipster-etl-s3-sns-lambda-transform"
  description      = "zipster-etl-s3-sns-lambda-transform"
}

resource "aws_lambda_function" "zipster-etl-s3-sns-lambda-load" {
  role             = aws_iam_role.zipster-etl-s3-sns-lambda-load-role.arn
  handler          = "etl-load.lambda_handler"
  runtime          = "python3.6"
  filename         = data.archive_file.zipit_lambda_etl_load.output_path
  source_code_hash = data.archive_file.zipit_lambda_etl_load.output_base64sha256
  function_name    = "zipster-etl-s3-sns-lambda-load"
  description      = "zipster-etl-s3-sns-lambda-load"
  environment {
    variables = {
      DB_HOST = aws_instance.ec2_mysql[0].public_dns
    }
  }
}

resource "aws_iam_role" "zipster-etl-s3-sns-lambda-transform-role" {
  name        = "zipster-etl-s3-sns-lambda-transform-role"
  path        = "/"
  description = "Allows Lambda Function to call AWS lambda services on your behalf."
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role" "zipster-etl-s3-sns-lambda-load-role" {
  name        = "zipster-etl-s3-sns-lambda-load-role"
  path        = "/"
  description = "Allows Lambda Function to call AWS lambda services on your behalf."
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}


resource "aws_lambda_permission" "zipster-etl-s3-sns-lambda-bucket-transform-input-s3-permission-lambda-transformation" {
  statement_id  = "zipster-etl-s3-sns-lambda-bucket-transform-input-s3-permission-lambda-transformation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-transform-input.arn
}

resource "aws_lambda_permission" "zipster-etl-s3-sns-lambda-bucket-load-input-s3-permission-lambda-transformation" {
  statement_id  = "zipster-etl-s3-sns-lambda-bucket-load-input-s3-permission-lambda-transformation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-load.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-load-input.arn
}

resource "aws_lambda_permission" "zipster-etl-s3-sns-lambda-bucket-transform-error-s3-permission-lambda-transformation" {
  statement_id  = "zipster-etl-s3-sns-lambda-bucket-transform-error-s3-permission-lambda-transformation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-transform-error.arn
}

resource "aws_lambda_permission" "zipster-etl-s3-sns-lambda-transform-allow-events" {
  statement_id  = "zipster-etl-s3-sns-lambda-transform-allow-events"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.arn
}

resource "aws_lambda_permission" "zipster-etl-s3-sns-lambda-load-allow-events" {
  statement_id  = "zipster-etl-s3-sns-lambda-load-allow-events"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-load.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_lambda_function.zipster-etl-s3-sns-lambda-load.arn
}

resource "aws_iam_policy" "zipster-etl-s3-sns-lambda-transform-log" {
  name = "zipster-etl-s3-sns-lambda-transform-log"
  path = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents","logs:DescribeLogStreams"],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "zipster-etl-s3-sns-lambda-load-log" {
  name = "zipster-etl-s3-sns-lambda-load-log"
  path = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents","logs:DescribeLogStreams"],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "zipster-etl-s3-sns-lambda-bucket-transform-input-lambda-access" {
  name = "zipster-etl-s3-sns-lambda-bucket-transform-input-lambda-access"
  path = "/"
  description = "IAM policy for accessing s3 from zipster-etl-s3-sns-lambda-bucket-transform-lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "arn:aws:s3:::zipster-etl-s3-sns-lambda-bucket-transform-input/*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "zipster-etl-s3-sns-lambda-bucket-load-input-lambda-access" {
  name = "zipster-etl-s3-sns-lambda-bucket-transform-load-lambda-access"
  path = "/"
  description = "IAM policy for accessing s3 from zipster-etl-s3-sns-lambda-load"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "arn:aws:s3:::zipster-etl-s3-sns-lambda-bucket-load-input/*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "zipster-etl-s3-sns-lambda-bucket-transform-error-lambda-access" {
  name = "zipster-etl-s3-sns-lambda-bucket-transform-error-lambda-access"
  path = "/"
  description = "IAM policy for accessing s3 from zipster-etl-s3-sns-lambda-transform"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "arn:aws:s3:::zipster-etl-s3-sns-lambda-bucket-transform-error/*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "lambda_access_sns_listtopics_publish_subscribe" {
  name = "lambda_access_sns_list"
  path = "/"
  description = "IAM policy for lambda to have listtopics, publish and subscribe access to SNS"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["sns:ListTopics", "sns:Publish", "sns:Subscribe"],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "lambda-logging" {
  name = "lambda-logging"
  path = "/"
  description = "IAM policy for logging from a lambda so CloudWatch can be used"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-transform-role-lambda-logging" {
  role = aws_iam_role.zipster-etl-s3-sns-lambda-transform-role.name
  policy_arn = aws_iam_policy.lambda-logging.arn
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-load-role-lambda-logging" {
  role = aws_iam_role.zipster-etl-s3-sns-lambda-load-role.name
  policy_arn = aws_iam_policy.lambda-logging.arn
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-transform-role-for-zipster-etl-s3-sns-lambda-bucket-transform-input-lambda-access" {
  role = aws_iam_role.zipster-etl-s3-sns-lambda-transform-role.name
  policy_arn = aws_iam_policy.zipster-etl-s3-sns-lambda-bucket-transform-input-lambda-access.arn
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-load-role-for-zipster-etl-s3-sns-lambda-bucket-load-input-lambda-access" {
  role = aws_iam_role.zipster-etl-s3-sns-lambda-load-role.name
  policy_arn = aws_iam_policy.zipster-etl-s3-sns-lambda-bucket-load-input-lambda-access.arn
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-load-role-for-zipster-etl-s3-sns-lambda-bucket-transform-error-lambda-access" {
  role = aws_iam_role.zipster-etl-s3-sns-lambda-transform-role.name
  policy_arn = aws_iam_policy.zipster-etl-s3-sns-lambda-bucket-transform-error-lambda-access.arn
}

resource "aws_lambda_permission" "AllowAllAccessProcessEtl" {
  statement_id  = "AllowAllAccess"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.arn
  principal     = "sns.amazonaws.com"
}

resource "aws_lambda_permission" "AllowAllAccessProcessSqlProcess" {
  statement_id  = "AllowAllAccess"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zipster-etl-s3-sns-lambda-load.arn
  principal     = "sns.amazonaws.com"
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-transform-role-for-lambda_access_sns_listtopics_publish_subscribe" {
  role       = aws_iam_role.zipster-etl-s3-sns-lambda-transform-role.name
  policy_arn = aws_iam_policy.lambda_access_sns_listtopics_publish_subscribe.arn
}

resource "aws_iam_role_policy_attachment" "zipster-etl-s3-sns-lambda-load-role-for-lambda_access_sns_listtopics_publish_subscribe" {
  role       = aws_iam_role.zipster-etl-s3-sns-lambda-load-role.name
  policy_arn = aws_iam_policy.lambda_access_sns_listtopics_publish_subscribe.arn
}







