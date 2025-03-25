#!/usr/bin/env python3
"""
Test suite for infrastructure and API
"""

import unittest
import json
import os
import sys
import subprocess
import requests
import time
import docker
from typing import Dict, Any, List, Optional
import pytest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestInfrastructure(unittest.TestCase):
    """Test infrastructure deployment with Terraform and LocalStack"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Start LocalStack if not already running
        cls.ensure_localstack_running()

        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd="terraform", check=True)

        # Apply Terraform with LocalStack provider
        cls.tf_apply = subprocess.run(
            ["terraform", "apply", "-var-file=local.tfvars", "-auto-approve"],
            cwd="terraform",
            capture_output=True,
            text=True,
        )

        # Wait for resources to be available
        time.sleep(5)

        # Get outputs
        cls.outputs = cls.get_terraform_outputs()

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment"""
        # Destroy Terraform resources
        subprocess.run(
            ["terraform", "destroy", "-var-file=local.tfvars", "-auto-approve"],
            cwd="terraform",
        )

    @classmethod
    def ensure_localstack_running(cls):
        """Ensure LocalStack is running"""
        client = docker.from_env()

        # Check if LocalStack container is running
        containers = client.containers.list(filters={"name": "localstack"})

        if not containers:
            print("Starting LocalStack container...")
            client.containers.run(
                "localstack/localstack:latest",
                name="localstack",
                detach=True,
                ports={"4566/tcp": 4566},
                environment={
                    "SERVICES": "s3,dynamodb,rds,ecs,ec2,iam,lambda,logs,sqs",
                    "DEFAULT_REGION": "us-east-1",
                    "DEBUG": "1",
                },
            )
            # Wait for LocalStack to initialize
            time.sleep(15)

    @classmethod
    def get_terraform_outputs(cls) -> Dict[str, Any]:
        """Get Terraform outputs"""
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd="terraform",
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_terraform_apply_success(self):
        """Test that Terraform apply succeeded"""
        self.assertEqual(
            self.tf_apply.returncode,
            0,
            f"Terraform apply failed: {self.tf_apply.stderr}",
        )

    def test_vpc_created(self):
        """Test that VPC was created"""
        self.assertIn("vpc_id", self.outputs)
        self.assertIsNotNone(self.outputs["vpc_id"]["value"])

    def test_rds_endpoint_created(self):
        """Test that RDS endpoint was created"""
        self.assertIn("rds_endpoint", self.outputs)
        self.assertIsNotNone(self.outputs["rds_endpoint"]["value"])

    def test_alb_dns_created(self):
        """Test that ALB DNS was created"""
        self.assertIn("alb_dns_name", self.outputs)
        self.assertIsNotNone(self.outputs["alb_dns_name"]["value"])


class TestAPI(unittest.TestCase):
    """Test the FastAPI application"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Start API container if not already running
        cls.ensure_api_running()

        # Base URL for API
        cls.api_base_url = "http://localhost:8000"

        # Wait for API to be ready
        cls.wait_for_api()

    @classmethod
    def ensure_api_running(cls):
        """Ensure API container is running"""
        client = docker.from_env()

        # Check if API container is running
        containers = client.containers.list(filters={"name": "backend-api"})

        if not containers:
            print("Starting API container...")
            # Build the image first
            subprocess.run(
                ["docker", "build", "-t", "backend-api:local", "."], check=True
            )

            # Run the container
            client.containers.run(
                "backend-api:local",
                name="backend-api",
                detach=True,
                ports={"8000/tcp": 8000},
                environment={
                    "DB_HOST": "localstack",
                    "DB_PORT": "5432",
                    "DB_NAME": "postgres",
                    "DB_USER": "postgres",
                    "DB_PASSWORD": "postgres",
                    "ENV": "test",
                },
                network="backend-network",
            )
            # Wait for API to initialize
            time.sleep(5)

    @classmethod
    def wait_for_api(cls, timeout=30, interval=1):
        """Wait for API to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{cls.api_base_url}/health")
                if response.status_code == 200:
                    print("API is ready")
                    return
            except requests.RequestException:
                pass
            time.sleep(interval)
        raise TimeoutError("API did not become ready in time")

    def test_health_endpoint(self):
        """Test health endpoint"""
        response = requests.get(f"{self.api_base_url}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")

    def test_db_connection(self):
        """Test database connection via API endpoint"""
        response = requests.get(f"{self.api_base_url}/health/db")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["database"], "connected")

    def test_create_resource(self):
        """Test creating a resource"""
        payload = {"name": "test_resource", "description": "Test description"}
        response = requests.post(f"{self.api_base_url}/resources", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], payload["name"])
        self.assertIn("id", data)

        # Clean up - delete resource
        resource_id = data["id"]
        delete_response = requests.delete(
            f"{self.api_base_url}/resources/{resource_id}"
        )
        self.assertEqual(delete_response.status_code, 204)


@pytest.mark.integration
def test_full_deployment_pipeline():
    """Test the full deployment pipeline"""
    # This test can be run with pytest -m integration

    # Step 1: Deploy infrastructure
    deploy_result = subprocess.run(
        [
            "python",
            "scripts/deploy.py",
            "--action",
            "apply",
            "--env",
            "local",
            "--auto-approve",
        ],
        capture_output=True,
        text=True,
    )
    assert deploy_result.returncode == 0, f"Deployment failed: {deploy_result.stderr}"

    # Step 2: Run database migrations
    migrate_result = subprocess.run(
        ["python", "scripts/run_migrations.py"], capture_output=True, text=True
    )
    assert migrate_result.returncode == 0, f"Migrations failed: {migrate_result.stderr}"

    # Step 3: Build and deploy container
    container_result = subprocess.run(
        ["python", "scripts/deploy_container.py"], capture_output=True, text=True
    )
    assert (
        container_result.returncode == 0
    ), f"Container deployment failed: {container_result.stderr}"

    # Step 4: Test API health
    time.sleep(5)  # Wait for API to start
    health_response = requests.get("http://localhost:8000/health")
    assert health_response.status_code == 200

    # Step 5: Clean up
    cleanup_result = subprocess.run(
        [
            "python",
            "scripts/deploy.py",
            "--action",
            "destroy",
            "--env",
            "local",
            "--auto-approve",
        ],
        capture_output=True,
        text=True,
    )
    assert cleanup_result.returncode == 0, f"Cleanup failed: {cleanup_result.stderr}"


if __name__ == "__main__":
    unittest.main()
