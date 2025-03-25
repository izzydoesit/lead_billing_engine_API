# tests/test_infrastructure/test_terraform.py
import os
import json
import pytest
import subprocess
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    result = subprocess.run(
        command, shell=True, cwd=cwd, capture_output=True, text=True
    )
    return result


@pytest.fixture(scope="module")
def tf_init():
    """Initialize Terraform"""
    result = run_command("terraform init", cwd=os.path.join(PROJECT_ROOT, "terraform"))
    assert result.returncode == 0, f"Terraform init failed: {result.stderr}"
    return True


def test_terraform_validate(tf_init):
    """Test that Terraform configuration is valid"""
    result = run_command(
        "terraform validate", cwd=os.path.join(PROJECT_ROOT, "terraform")
    )
    assert result.returncode == 0, f"Terraform validation failed: {result.stderr}"
    assert "Success!" in result.stdout, "Terraform validation did not succeed"


def test_terraform_plan(tf_init):
    """Test that Terraform plan can be created"""
    result = run_command(
        "terraform plan -var-file=local.tfvars -no-color",
        cwd=os.path.join(PROJECT_ROOT, "terraform"),
    )
    assert result.returncode == 0, f"Terraform plan failed: {result.stderr}"

    # Check for expected resources in plan output
    expected_resources = ["aws_vpc", "aws_subnet", "aws_db_instance", "aws_ecs_cluster"]

    for resource in expected_resources:
        assert (
            resource in result.stdout
        ), f"Expected resource {resource} not found in plan"


def test_terraform_providers():
    """Test that Terraform providers.tf is correctly configured for LocalStack"""
    providers_file = os.path.join(PROJECT_ROOT, "terraform", "providers.tf")
    assert os.path.exists(providers_file), "providers.tf file does not exist"

    with open(providers_file, "r") as f:
        content = f.read()

    # Check for LocalStack configuration
    assert (
        "skip_credentials_validation = true" in content
    ), "Missing LocalStack configuration"
    assert "endpoints {" in content, "Missing LocalStack endpoints configuration"
    assert "http://localhost:4566" in content, "Incorrect LocalStack endpoint URL"


def test_terraform_variables():
    """Test that Terraform variables.tf contains all required variables"""
    variables_file = os.path.join(PROJECT_ROOT, "terraform", "variables.tf")
    assert os.path.exists(variables_file), "variables.tf file does not exist"

    with open(variables_file, "r") as f:
        content = f.read()

    # Check for required variables
    required_variables = [
        "aws_region",
        "project_name",
        "vpc_cidr",
        "db_username",
        "db_password",
    ]

    for var in required_variables:
        assert f'variable "{var}"' in content, f"Required variable {var} not found"


def test_docker_compose_configuration():
    """Test that docker-compose.yaml contains all required services"""
    docker_compose_file = os.path.join(PROJECT_ROOT, "docker-compose.yaml")
    assert os.path.exists(
        docker_compose_file
    ), "docker-compose.yaml file does not exist"

    with open(docker_compose_file, "r"):
        print(r)
