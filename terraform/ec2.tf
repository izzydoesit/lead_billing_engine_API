resource "aws_instance" "billing_server" {
  ami           = var.ami
  instance_type = var.instance_type
  tags = {
    "service" = "billing"
    Name      = var.name_tag
  }
}

resource "aws_instance" "lead_server" {
  ami           = var.ami
  instance_type = var.instance_type
  tags = {
    "service" = "leads"
    Name      = var.name_tag
  }
}

# # TODO: implement EC2 module w/ AMI & security groups
# module "ec2_instance" {
#   source  = "terraform-aws-modules/ec2-instance/aws"

#   name = "single-instance"

#   instance_type          = var.instance_type
#   key_name               = "user1"
#   monitoring             = true
#   vpc_security_group_ids = ["sg-12345678"]
#   subnet_id              = "subnet-eddcdzz4"

#   tags = {
#     Terraform   = "true"
#     Environment = "dev"
#   }
# }