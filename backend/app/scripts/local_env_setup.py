#!/usr/bin/env python3
"""
Local Environment Setup Script
This script sets up the local development environment for the backend API
"""

import os
import sys
import subprocess
import argparse
import json
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
TERRAFORM_DIR = PROJECT_ROOT / "terraform"
APP_DIR = PROJECT_ROOT / "app"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def setup_directories():
    """Ensure all required directories exist"""
    dirs = [
        TERRAFORM_DIR,
        APP_DIR / "migrations",
        APP_DIR / "models",
        APP_DIR / "schemas",
        APP_DIR / "routers",
        APP_DIR / "services",
        APP_DIR / "tests",
        SCRIPTS_DIR,
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Directory created/verified: {d}")


def create_terraform_local_config():
    """Create LocalStack Terraform configuration"""
    # Create provider.tf for LocalStack
    localstack_provider = """
provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  
  # LocalStack endpoint configuration
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    apigateway     = "http://localstack:4566"
    cloudformation = "http://localstack:4566"
    cloudwatch     = "http://localstack:4566"
    ec2            = "http://localstack:4566"
    iam            = "http://localstack:4566"
    rds            = "http://localstack:4566"
    s3             = "http://localstack:4566"
    secretsmanager = "http://localstack:4566"
  }
}
"""
    with open(TERRAFORM_DIR / "provider_local.tf", "w") as f:
        f.write(localstack_provider)

    # Create local.tfvars
    local_tfvars = """
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
"""
    with open(TERRAFORM_DIR / "local.tfvars", "w") as f:
        f.write(local_tfvars)

    print("Terraform local configuration created.")


def create_alembic_config():
    """Create Alembic configuration for database migrations"""
    alembic_ini = """
[alembic]
script_location = app/migrations
prepend_sys_path = .
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
    with open(PROJECT_ROOT / "alembic.ini", "w") as f:
        f.write(alembic_ini)

    # Create env.py
    migrations_dir = APP_DIR / "migrations"
    versions_dir = migrations_dir / "versions"
    versions_dir.mkdir(exist_ok=True)

    env_py = """
from logging.config import fileConfig
import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import our models metadata
from app.core.database import Base
from app.models import *

# This is the Alembic Config object
config = context.config

# Parse database url from environment
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.get
"""
