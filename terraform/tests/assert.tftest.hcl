provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

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

run "verify_vpc_ip_address_range" {
  command = plan

  assert {
    condition     = output.vpc_cidr_block == var.base_cidr_block
    error_message = "VPC CIDR block value does not match"
  }
}

run "verify_nat_elastic_ip" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_nat_gateway" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_internet_gateway" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_subnet_one" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_subnet_two" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_subnet_one" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_subnet_two" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_route_table" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_route_one" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_route_table" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_route_one" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_route_table_association_in_az1" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_private_route_table_association_in_az2" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_route_table_association_in_az1" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_public_route_table_association_in_az2" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_ec2_instance_leads" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}

run "verify_ec2_instance_billing" {
  command = plan

  assert {
    condition     = output
    error_message = "Value does not match"
  }
}
