# # VPC
output "vpc_id" {
  description = "The ID of the VPC that this stack is deployed in"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "The ID of the VPC that this stack is deployed in"
  value       = aws_vpc.main.cidr_block
}
