resource "aws_s3_bucket" "zipster-etl-s3-sns-lambda-bucket-transform-input" {
  bucket        = "zipster-etl-s3-sns-lambda-bucket-transform-input"
  acl           = "public-read-write"
  force_destroy = true
}

resource "aws_s3_bucket_notification" "zipster-etl-s3-sns-lambda-bucket-transform-input-lambda-notification" {
  bucket                = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-transform-input.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.arn
    events              = ["s3:ObjectCreated:Put"]
  }
}

resource "aws_s3_bucket" "zipster-etl-s3-sns-lambda-bucket-load-input" {
  bucket        = "zipster-etl-s3-sns-lambda-bucket-load-input"
  acl           = "public-read-write"
  force_destroy = true
}

resource "aws_s3_bucket_notification" "zipster-etl-s3-sns-lambda-bucket-load-input-lambda-notification" {
  bucket                = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-load-input.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.zipster-etl-s3-sns-lambda-load.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_s3_bucket" "zipster-etl-s3-sns-lambda-bucket-transform-error" {
  bucket        = "zipster-etl-s3-sns-lambda-bucket-transform-error"
  acl           = "public-read-write"
  force_destroy = true
}

#resource "aws_s3_bucket_notification" "zipster-etl-s3-sns-lambda-bucket-transform-error-lambda-notification" {
#  bucket                = aws_s3_bucket.zipster-etl-s3-sns-lambda-bucket-transform-error.id
#
#  lambda_function {
#    lambda_function_arn = aws_lambda_function.zipster-etl-s3-sns-lambda-transform.arn
#    events              = ["s3:ObjectCreated:Put"]
#  }
#}