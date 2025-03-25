
# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "billing-net"
}

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

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "container_port" {
  description = "Port the container exposes"
  type        = number
  default     = 8000
}

variable "container_image" {
  description = "Docker image for the application"
  type        = string
  default     = "your-ecr-repo/backend-app:latest"
}

variable "health_check_path" {
  description = "Path for health check"
  type        = string
  default     = "/health"
}

variable "app_count" {
  description = "Number of instances of the task to run"
  type        = number
  default     = 2
}

variable "task_cpu" {
  description = "CPU for the task definition"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Memory for the task definition"
  type        = string
  default     = "512"
}

variable "db_allocated_storage" {
  description = "Allocated storage for the database in GB"
  type        = number
  default     = 20
}

variable "db_engine" {
  description = "Database engine"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "14"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "dbadmin"
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
  default     = var.env_aws_db_password
}

variable "db_host" {
  description = "Host for RDS Database"
  type        = string
  sensitive   = true
  default     = var.env_aws_db_host
}

variable "db_port" {
  description = "Port for RDS Database"
  type        = integer
  sensitive   = true
  default     = var.env_aws_db_port
}

variable "db_name" {
  description = "Database name for RDS Database"
  type        = string
  sensitive   = true
  default     = var.env_aws_db_name
}

variable "db_multi_az" {
  description = "Multi-AZ deployment for RDS"
  type        = bool
  default     = false
}
