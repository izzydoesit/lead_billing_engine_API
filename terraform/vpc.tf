# VPC is isolated cloud environment to launch AWS resources in
# Specify IP address range for your VPC
# NEEDS: Subnets (range of IP addresses) to launch AWS resources into
# NEEDS: Security groups to control access
# NEEDS: Internet Gateway to connect to public internet
# NEEDS: Route tables to control traffic routing to/from subnets

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "billingvpc"
  }
}
