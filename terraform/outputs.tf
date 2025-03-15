data "aws_caller_identity" "current" {}
output "is_localstack" {
  value = data.aws_caller_identity.current.id == "000000000000"
}
