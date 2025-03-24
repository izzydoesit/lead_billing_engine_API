Local Terraform Variables

# local.tfvars - Configuration for local development

aws_region          = "us-east-1"
project_name        = "backend-app-local"
vpc_cidr            = "10.0.0.0/16"
availability_zones  = ["us-east-1a", "us-east-1b"]
container_port      = 8000
container_image     = "backend-api:local"
health_check_path   = "/health"
app_count           = 1
task_cpu            = "256"
task_memory         = "512"
db_allocated_storage = 20
db_engine           = "postgres"
db_engine_version   = "14"
db_instance_class   = "db.t3.micro"
db_username         = "postgres"
db_password         = "postgres"
db_multi_az         = false