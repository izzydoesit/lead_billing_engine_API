terraform {
  required_version = ">= 0.12"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.region
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = false

  endpoints {
    apigateway = "http://localstack:4566"
    ecs        = "http://localstack:4566"
    rds        = "http://localstack:4566"
    iam        = "http://localstack:4566"
    ec2        = "http://localstack:4566"
    # Add other services as needed
    s3 = "http://s3.localhost.localstack.cloud:4566"
  }
}
