# # VPC
variable "base_cidr_block" {
  type    = string
  default = "10.0.0.0/16"
  validation {
    condition     = split("/", var.base_cidr_block)[1] >= 16 && split("/", var.base_cidr_block)[1] <= 28
    error_message = "Your vpc cidr is not between 16 and 28"
  }
}

variable "ami" {
  description = "The AMI to use for the instance"
  type        = string
}

variable "instance_type" {
  description = "The type of instance to create"
  type        = string
}

variable "name_tag" {
  description = "The name tag for the resource"
  type        = string
}