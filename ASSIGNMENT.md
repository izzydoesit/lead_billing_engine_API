# Internal Engineering Team Software Engineer Interview Project

### Project Overview

We invite you to develop a Lead Billing Engine that processes leads based on their types and actions, assigns values
accordingly, and generates detailed billing reports for customers. This project will assess your ability to design and
implement a full-stack solution, including infrastructure provisioning, backend development, database management, and
deployment automation.

### Definitions
##### 1. Lead
   A Lead is a potential customer who has expressed interest in a company's products or services.
```
Example:
John@yahoo.com fills out a form on your website to learn more about Product ABC.
```
##### 2. Billing
  Billing is the process of charging our B2B partners that offers the products and services to end customers. 
```
Example:
Acme Corporation receives a monthly bill for the 50 leads generated for their Product ABC in April.
```

### Context and Background

Our business relies on generating and processing various types of leads. Each lead contains specific actions that are
categorized based on their engagement levels. More engaging actions are deemed more valuable, impacting how customers
are billed for the leads they utilize. The Billing Engine must accurately recognize different lead types, evaluate
actions, assign appropriate values, and produce comprehensive billing reports.

### Sample Leads JSON

Below is a sample of the leads data your Billing Engine will process:

<details>

```json
[
  {
    "lead_id": "uuid-1",
    "customer_id": "customer-123",
    "product_id": "product-abc",
    "lead_type": "Website Visit",
    "actions": [
      {
        "action_type": "Page View",
        "timestamp": "2024-04-01T10:00:00Z",
        "engagement_level": "Low"
      },
      {
        "action_type": "Form Submission",
        "timestamp": "2024-04-01T10:05:00Z",
        "engagement_level": "High"
      }
    ],
    "created_at": "2024-04-01T09:55:00Z"
  },
  {
    "lead_id": "uuid-2",
    "customer_id": "customer-456",
    "product_id": "product-def",
    "lead_type": "Social Media",
    "actions": [
      {
        "action_type": "Like",
        "timestamp": "2024-04-02T11:00:00Z",
        "engagement_level": "Low"
      },
      {
        "action_type": "Share",
        "timestamp": "2024-04-02T11:10:00Z",
        "engagement_level": "Medium"
      }
    ],
    "created_at": "2024-04-02T10:50:00Z"
  },
  {
    "lead_id": "uuid-3",
    "customer_id": "customer-123",
    "product_id": "product-abc",
    "lead_type": "Website Visit",
    "actions": [
      {
        "action_type": "Form Submission",
        "timestamp": "2024-04-15T12:00:00Z",
        "engagement_level": "High"
      }
    ],
    "created_at": "2024-04-15T11:55:00Z"
  },
  {
    "lead_id": "uuid-4",
    "customer_id": "customer-123",
    "product_id": "product-xyz",
    "lead_type": "Website Visit",
    "actions": [
      {
        "action_type": "Form Submission",
        "timestamp": "2024-05-05T09:00:00Z",
        "engagement_level": "High"
      }
    ],
    "created_at": "2024-05-05T08:55:00Z"
  }
]

```

</details>

### Assignment Objectives

- Infrastructure Provisioning: Utilize Terraform to set up all necessary infrastructure locally using LocalStack,
including API Gateway, ECS Fargate, PostgreSQL database, and other required services.

- Backend Development: Develop a RESTful API using FastAPI (preferred) that processes leads, calculates billing based on
lead types and actions, and generates billing reports.

- Database Management: Design and manage a PostgreSQL database schema to store leads, actions, customers, and billing
information. Implement ORM handling and migrations.

- Deployment Automation: Create scripts to automate the setup of infrastructure, deployment of the backend service, and
database migrations, ensuring the entire environment can be brought up locally with ease.

### Detailed Requirements

### 1. Infrastructure as Code (Terraform)
   LocalStack Configuration: Ensure that all AWS services used (API Gateway, ECS Fargate, RDS PostgreSQL, etc.) are
   provisioned locally via LocalStack. Candidates are opened to use **open source terraform modules to save time**. 

Terraform Scripts:

* VPC Setup: Create a Virtual Private Cloud with appropriate subnets and security groups.
* ECS Cluster: Set up an ECS Cluster using the Fargate launch type.
* (BONUS POINTS - see below section 6.)API Gateway: Configure API Gateway to handle HTTP requests and route them to ECS services.
* RDS PostgreSQL: Provision a PostgreSQL database instance.
* IAM Roles and Policies: Define necessary roles and policies for ECS tasks and other services.
* Networking: Configure security groups and networking rules to allow communication between services.

### 2. Backend Development
   Framework: FastAPI is preferred for its performance and ease of use, but candidates may choose other Python/Golang
   Frameworks if they prefer.

Billing Logic:

* Lead Evaluation: Assess leads based on lead_type and actions.
* Action Valuation: Assign monetary values to actions based on their engagement_level (e.g., High = $10, Medium = $5,
  Low = $2).
* Billing Calculation: Aggregate the values of actions to compute the total billing amount per lead and per customer.
* Business Logic:
  * Lead Recognition: Differentiate between lead types and apply appropriate billing rules.
  * Error Handling: Manage scenarios such as invalid data, duplicate leads, missing fields, and system failures.
  * Duplicate Lead Detection: Ensure that duplicate leads (same user, same action type, same engagement level) are not charged multiple times and recorded as savings in the billing report.
  * Billing Cap Implementation: Apply a billing cap of $100 per lead user. Any charges beyond this cap should not be billed but recorded as savings in the billing report.
  * Product Association: Differentiate leads based on product_id. Leads with the same user and action types but different products should be treated as separate and billed independently.
  

* Database Integration:
  * ORM: Use an ORM (e.g., SQLAlchemy for Python) for database interactions.
  * Migrations: Implement database migrations to handle schema changes. Eg: Alembic for Python

### 3. Database Schema
   Design a PostgreSQL database with the following tables:

#### Customers:

* customer_id (UUID, Primary Key)
* name (String, Not Null)
* email (String, Unique, Not Null)
* created_at (Timestamp)

#### Leads:

* lead_id (UUID, Primary Key)
* customer_id (UUID, Foreign Key to Customers)
* lead_type (String, e.g., "Website Visit", "Social Media")
* created_at (Timestamp)

#### Products:
* product_id (UUID, Primary Key)
* name (String, Not Null)
* description (Text, Optional)
* created_at (Timestamp)

#### Actions:
* -- To be added by candidates -- 


#### BillingReports:
* -- To be added by candidates --

#### ++ Additional Tables if applicable

### 4. Deployment and Automation
   Containerization: Dockerize the backend application for consistent deployment.

Terraform Deployment: Ensure that running Terraform scripts sets up all infrastructure components locally via
LocalStack.

Setup Scripts: Provide scripts (e.g., shell scripts, Makefile, Poetry Scripts) to automate:

1. Initialization of Terraform.
2. Deployment of infrastructure.
3. Building and deploying Docker containers.
4. Running database migrations.
5. Starting the backend service.
6. The entire setup should be deployable locally without dependencies on actual AWS services.
7. Seeding the database with sample data.
8. Generating a sample billing report.

### 5. Documentation
   Provide a comprehensive README.md that includes:

* Project Overview: Brief description of the Billing Engine and its components.

* Setup Instructions:

* Prerequisites (e.g., Docker, Terraform, LocalStack installation).
* Step-by-step guide to deploying infrastructure and running the application locally. (Although this should be highly automated)


* Database Schema: Explanation of the database design and relationships. Using dbdiagram.io yaml files as documentations are welcomed

* Billing Logic: Description of how leads and actions are evaluated and billed if there are any additional special logics incorporated. 

* Error Scenarios: Outline how the system handles common errors and edge cases.

* Scripts Usage: Instructions on how to use provided scripts for setup and deployment.
  * This may include seeding the database with sample lead data and other prepopulated data for testing purposes. 

* Sample Billing Reports: Sample billing reports generated by the Billing Engine. 

### 6. Bonus Points
#### Part I: Write unit tests for the Billing Engine.
- A full coverage is not necessary, but enough to cover critical paths. 

#### Part II: This assignment is backend heavy however it does have client facing components.
- Create the following: 
  - API Endpoints:
    * POST /leads: Ingest new leads data.
    * GET /billing/reports: Retrieve billing reports for customers.
    * GET /leads: Retrieve leads with filtering options (e.g., by customer, lead type).
  * API Gateway Infrastructure integrated with the endpoints above. 



### References: 
Below are some useful resources to help you kickstart on your project.
- [LocalStack with Terraform](https://docs.localstack.cloud/user-guide/integrations/terraform/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)
- [Dbdiagram.io](https://dbdiagram.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org)
- [Faker](https://faker.readthedocs.io/en/master/)