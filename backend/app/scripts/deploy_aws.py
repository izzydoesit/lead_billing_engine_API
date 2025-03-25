#!/usr/bin/env python3
"""
AWS Infrastructure Deployment Script
This script handles the deployment of AWS infrastructure using Terraform
"""

"""
POPULATE CONFIG.JSON FILE THEN RUN THIS FILE:

python deploy_aws.py --action plan --env dev --config config.json
python deploy_aws.py --action apply --env dev --config config.json --auto-approve
"""

import os
import sys
import subprocess
import argparse
import json
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class TerraformDeployer:
    def __init__(self, working_dir: str = "."):
        self.working_dir = working_dir

    def initialize(self) -> bool:
        """Initialize Terraform"""
        logger.info("Initializing Terraform...")
        result = self._run_command(["terraform", "init"])
        return result.returncode == 0

    def validate(self) -> bool:
        """Validate Terraform configuration"""
        logger.info("Validating Terraform configuration...")
        result = self._run_command(["terraform", "validate"])
        return result.returncode == 0

    def plan(self, var_file: str = None, out_file: str = "tfplan") -> bool:
        """Create Terraform execution plan"""
        logger.info("Creating Terraform execution plan...")
        command = ["terraform", "plan"]

        if var_file:
            command.extend(["-var-file", var_file])

        command.extend(["-out", out_file])

        result = self._run_command(command)
        return result.returncode == 0

    def apply(self, plan_file: str = "tfplan", auto_approve: bool = False) -> bool:
        """Apply Terraform execution plan"""
        logger.info("Applying Terraform execution plan...")
        command = ["terraform", "apply"]

        if auto_approve:
            command.append("-auto-approve")

        if plan_file:
            command.append(plan_file)

        result = self._run_command(command)
        return result.returncode == 0

    def destroy(self, var_file: str = None, auto_approve: bool = False) -> bool:
        """Destroy the infrastructure"""
        logger.info("Destroying infrastructure...")
        command = ["terraform", "destroy"]

        if auto_approve:
            command.append("-auto-approve")

        if var_file:
            command.extend(["-var-file", var_file])

        result = self._run_command(command)
        return result.returncode == 0

    def output(self, json_format: bool = True) -> Dict[str, Any]:
        """Get Terraform outputs"""
        logger.info("Getting Terraform outputs...")
        command = ["terraform", "output"]

        if json_format:
            command.append("-json")

        result = self._run_command(command)

        if result.returncode != 0:
            return {}

        if json_format:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                logger.error("Failed to parse Terraform output as JSON")
                return {}

        return {"raw_output": result.stdout}

    def workspace_list(self) -> List[str]:
        """List Terraform workspaces"""
        result = self._run_command(["terraform", "workspace", "list"])
        if result.returncode != 0:
            return []

        workspaces = result.stdout.strip().split("\n")
        # Remove the "*" from current workspace
        workspaces = [w.replace("* ", "") for w in workspaces]
        return workspaces

    def workspace_select(self, name: str) -> bool:
        """Select a Terraform workspace"""
        logger.info(f"Selecting workspace: {name}")
        result = self._run_command(["terraform", "workspace", "select", name])
        return result.returncode == 0

    def workspace_new(self, name: str) -> bool:
        """Create a new Terraform workspace"""
        logger.info(f"Creating new workspace: {name}")
        result = self._run_command(["terraform", "workspace", "new", name])
        return result.returncode == 0

    def _run_command(self, command: List[str]) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        try:
            return subprocess.run(
                command,
                cwd=self.working_dir,
                check=False,
                capture_output=True,
                text=True,
            )
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            # Return a fake CompletedProcess with error code
            return subprocess.CompletedProcess(
                args=command, returncode=1, stdout="", stderr=str(e)
            )


def create_var_file(env: str, config: Dict[str, Any]) -> str:
    """Create a Terraform variable file from config"""
    filename = f"{env}.tfvars"
    with open(filename, "w") as f:
        for key, value in config.items():
            if isinstance(value, str):
                f.write(f'{key} = "{value}"\n')
            else:
                f.write(f"{key} = {value}\n")
    return filename


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Deploy AWS infrastructure using Terraform"
    )

    parser.add_argument(
        "--action",
        choices=["plan", "apply", "destroy", "output"],
        required=True,
        help="Action to perform",
    )

    parser.add_argument(
        "--env",
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment to deploy to",
    )

    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Automatically approve apply/destroy actions",
    )

    parser.add_argument("--config", type=str, help="Path to configuration file")

    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()

    # Load config if provided
    config = {}
    if args.config and os.path.exists(args.config):
        try:
            with open(args.config, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse config file: {args.config}")
            sys.exit(1)

    # Create deployer
    deployer = TerraformDeployer()

    # Initialize Terraform
    if not deployer.initialize():
        logger.error("Terraform initialization failed")
        sys.exit(1)

    # Check if the workspace exists, create if not
    workspaces = deployer.workspace_list()
    if args.env not in workspaces:
        if not deployer.workspace_new(args.env):
            logger.error(f"Failed to create workspace: {args.env}")
            sys.exit(1)
    else:
        # Select the workspace
        if not deployer.workspace_select(args.env):
            logger.error(f"Failed to select workspace: {args.env}")
            sys.exit(1)

    # Validate the configuration
    if not deployer.validate():
        logger.error("Terraform validation failed")
        sys.exit(1)

    # Create var file if we have config
    var_file = None
    if config:
        var_file = create_var_file(args.env, config)
        logger.info(f"Created variable file: {var_file}")

    # Execute the requested action
    if args.action == "plan":
        # Create a plan
        plan_file = f"{args.env}.tfplan"
        if not deployer.plan(var_file=var_file, out_file=plan_file):
            logger.error("Terraform plan failed")
            sys.exit(1)
        logger.info(f"Plan created: {plan_file}")

    elif args.action == "apply":
        # Create and apply a plan
        plan_file = f"{args.env}.tfplan"
        if not deployer.plan(var_file=var_file, out_file=plan_file):
            logger.error("Terraform plan failed")
            sys.exit(1)

        if not deployer.apply(plan_file=plan_file, auto_approve=args.auto_approve):
            logger.error("Terraform apply failed")
            sys.exit(1)

        # Show outputs
        outputs = deployer.output()
        logger.info("Deployment outputs:")
        logger.info(json.dumps(outputs, indent=2))

    elif args.action == "destroy":
        # Destroy the infrastructure
        if not deployer.destroy(var_file=var_file, auto_approve=args.auto_approve):
            logger.error("Terraform destroy failed")
            sys.exit(1)
        logger.info(f"Infrastructure in {args.env} environment destroyed")

    elif args.action == "output":
        # Show outputs
        outputs = deployer.output()
        logger.info("Deployment outputs:")
        logger.info(json.dumps(outputs, indent=2))

    logger.info(f"Action '{args.action}' completed successfully")


if __name__ == "__main__":
    main()
