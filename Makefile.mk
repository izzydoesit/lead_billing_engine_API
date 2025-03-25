.PHONY: setup clean docker-build docker-up docker-down test test-integration \
		migrate migrate-down migrate-create seed terraform-init terraform-plan \
		terraform-apply terraform-destroy api-local help

# Colors for terminal output
COLOR_RESET=\033[0m
COLOR_GREEN=\033[32m
COLOR_YELLOW=\033[33m
COLOR_BLUE=\033[34m

# Docker related variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

# Terraform related variables
TERRAFORM_DIR = terraform
TERRAFORM_ENV ?= local

# Database migration related variables
MIGRATIONS_DIR = app/migrations

# Application variables
APP_MODULE = app.main:app
APP_PORT = 8000

help:
	@echo "${COLOR_BLUE}Backend API Development Commands${COLOR_RESET}"
	@echo ""
	@echo "${COLOR_GREEN}Setup Commands:${COLOR_RESET}"
	@echo "  make setup           - Set up development environment"
	@echo "  make clean           - Clean up generated files"
	@echo ""
	@echo "${COLOR_GREEN}Docker Commands:${COLOR_RESET}"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-up       - Start Docker containers"
	@echo "  make docker-down     - Stop Docker containers"
	@echo ""
	@echo "${COLOR_GREEN}Testing Commands:${COLOR_RESET}"
	@echo "  make test            - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo ""
	@echo "${COLOR_GREEN}Database Commands:${COLOR_RESET}"
	@echo "  make migrate         - Run database migrations"
	@echo "  make migrate-down    - Revert last migration"
	@echo "  make migrate-create name=migration_name - Create new migration"
	@echo "  make seed            - Seed database with sample data"
	@echo ""
	@echo "${COLOR_GREEN}Terraform Commands:${COLOR_RESET}"
	@echo "  make terraform-init  - Initialize Terraform"
	@echo "  make terraform-plan  - Create Terraform plan"
	@echo "  make terraform-apply - Apply Terraform configuration"
	@echo "  make terraform-destroy - Destroy Terraform resources"
	@echo ""
	@echo "${COLOR_GREEN}Application Commands:${COLOR_RESET}"
	@echo "  make api-local       - Run API locally"

setup:
	@echo "${COLOR_BLUE}Setting up development environment...${COLOR_RESET}"
	poetry install
	pre-commit install
	python scripts/setup_local_env.py
	@echo "${COLOR_GREEN}Setup complete!${COLOR_RESET}"

clean:
	@echo "${COLOR_BLUE}Cleaning up...${COLOR_RESET}"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .coverage
	@echo "${COLOR_GREEN}Cleanup complete!${COLOR_RESET}"

docker-build:
	@echo "${COLOR_BLUE}Building Docker images...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build
	@echo "${COLOR_GREEN}Docker images built!${COLOR_RESET}"

docker-up:
	@echo "${COLOR_BLUE}Starting Docker containers...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "${COLOR_GREEN}Docker containers started!${COLOR_RESET}"

docker-down:
	@echo "${COLOR_BLUE}Stopping Docker containers...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down
	@echo "${COLOR_GREEN}Docker containers stopped!${COLOR_RESET}"

test:
	@echo "${COLOR_BLUE}Running unit tests...${COLOR_RESET}"
	pytest -v tests/unit
	@echo "${COLOR_GREEN}Unit tests complete!${COLOR_RESET}"

test-integration:
	@echo "${COLOR_BLUE}Running integration tests...${COLOR_RESET}"
	pytest -v tests/integration
	@echo "${COLOR_GREEN}Integration tests complete!${COLOR_RESET}"

migrate:
	@echo "${COLOR_BLUE}Running database migrations...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api alembic upgrade head
	@echo "${COLOR_GREEN}Migrations complete!${COLOR_RESET}"

migrate-down:
	@echo "${COLOR_BLUE}Reverting last migration...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api alembic downgrade -1
	@echo "${COLOR_GREEN}Migration reverted!${COLOR_RESET}"

migrate-create:
	@echo "${COLOR_BLUE}Creating new migration: $(name)...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api alembic revision --autogenerate -m "$(name)"
	@echo "${COLOR_GREEN}Migration created!${COLOR_RESET}"

seed:
	@echo "${COLOR_BLUE}Seeding database...${COLOR_RESET}"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python -m scripts.seed_db
	@echo "${COLOR_GREEN}Database seeded!${COLOR_RESET}"

terraform-init:
	@echo "${COLOR_BLUE}Initializing Terraform...${COLOR_RESET}"
	cd $(TERRAFORM_DIR) && terraform init
	@echo "${COLOR_GREEN}Terraform initialized!${COLOR_RESET}"

terraform-plan:
	@echo "${COLOR_BLUE}Creating Terraform plan for $(TERRAFORM_ENV)...${COLOR_RESET}"
	cd $(TERRAFORM_DIR) && terraform plan -var-file=$(TERRAFORM_ENV).tfvars -out=$(TERRAFORM_ENV).tfplan
	@echo "${COLOR_GREEN}Terraform plan created!${COLOR_RESET}"

terraform-apply:
	@echo "${COLOR_BLUE}Applying Terraform configuration for $(TERRAFORM_ENV)...${COLOR_RESET}"
	cd $(TERRAFORM_DIR) && terraform apply $(TERRAFORM_ENV).tfplan
	@echo "${COLOR_GREEN}Terraform configuration applied!${COLOR_RESET}"

terraform-destroy:
	@echo "${COLOR_BLUE}Destroying Terraform resources for $(TERRAFORM_ENV)...${COLOR_RESET}"
	cd $(TERRAFORM_DIR) && terraform destroy -var-file=$(TERRAFORM_ENV).tfvars -auto-approve
	@echo "${COLOR_GREEN}Terraform resources destroyed!${COLOR_RESET}"

api-local:
	@echo "${COLOR_BLUE}Running API locally...${COLOR_RESET}"
	uvicorn $(APP_MODULE) --host 0.0.0.0 --port $(APP_PORT) --reload
	@echo "${COLOR_GREEN}API stopped!${COLOR_RESET}"

# Default target
.DEFAULT_GOAL := help