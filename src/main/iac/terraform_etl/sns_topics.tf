resource "aws_sns_topic" "zipster-etl-s3-sns-lambda-transform-topic" {
  name = "zipster-etl-s3-sns-lambda-transform-topic"
  provisioner "local-exec" {
    command = "aws sns subscribe --topic-arn ${self.arn} --protocol email --notification-endpoint howard.deiner@deinersoft.com"
  }
}

resource "aws_sns_topic" "zipster-etl-s3-sns-lambda-load-topic" {
  name = "zipster-etl-s3-sns-lambda-load-topic"
  provisioner "local-exec" {
    command = "aws sns subscribe --topic-arn ${self.arn} --protocol email --notification-endpoint howard.deiner@deinersoft.com"
  }
}
