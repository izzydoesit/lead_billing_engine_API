provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = false

  endpoints {
    apigateway     = "http://localhost:4566"
    apigatewayv2   = "http://localhost:4566"
    ec2            = "http://localhost:4566"
    ecs            = "http://localhost:4566"
    iam            = "http://localhost:4566"
    rds            = "http://localhost:4566"
    secretsmanager = "http://localhost:4566"
    # cloudformation = "http://localhost:4566"
    # cloudwatch     = "http://localhost:4566"
    # cloudwatchlogs = "http://localhost:4566"
    # s3             = "http://localhost:4566"
  }
}

variables {
  key = "value"
}

# run "check_vpc_id" {

#   command = apply

#   assert {
#     condition     = output.s3_bucket_name == var.s3_bucket_name
#     error_message = "VPC id does not match"
#   }

# }