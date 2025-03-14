provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_force_path_style         = true
  skip_requesting_account_id  = true

  resource "aws_s3_bucket" "test-bucket" {
    bucket = "my-bucket"
  }

  endpoints {
    apigateway     = "http://localstack:4566"
    ecs            = "http://localstack:4566"
    rds            = "http://localstack:4566"
    iam            = "http://localstack:4566"
    ec2            = "http://localstack:4566"
    # Add other services as needed
    s3             = "http://s3.localhost.localstack.cloud:4566"
  }
}

 resource "aws_s3_bucket" "test-bucket" {
    bucket = "my-bucket"
  }