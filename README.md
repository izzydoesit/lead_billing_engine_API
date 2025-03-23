# LEAD BILLING ENGINE

## Project Overview

The Lead Billing Engine is a powerful tool designed to streamline the billing process for leads. It automates the processing of leads, evaluates and assigns a corresponding dollar cost to each lead actions, and provides detailed reports on billing activities for our customers.

### Infrasturcture

first step is to configure your local environment for development. We are using LocalStack, which runs in a Docker container, and AWS Local CLI to simulate the AWS cloud environment locally.

1. Install LocalStack and AWS Local in your terminal
   `pip install localstack awscli-local`
2. Sign up for LocalStack-Pro and obtain your auth token then configure it in your terminal environment
   `export LOCALSTACK_AUTH_TOKEN=your_localstack_pro_token`
3. Verify your token is available in your environment
   `echo ${LOCALSTACK_AUTH_TOKEN}`
   Note: this is a temporary token, and you will need to set it every time you start a new terminal session.
4. Configure your AWS CLI with LocalStack
   `aws configure --profile localstack`
   - AWS Access Key ID: test
   - AWS Secret Access Key: test
   - Default region name: us-east-1
5. Start LocalStack in a local Docker container in detached mode (NOTE: make sure Docker Desktop is already running!)

```bash
    $> localstack start -d
```

6. Verify LocalStack is running in Docker via your terminal:

   ```bash
   $> docker ps
   OR
    localstack status
   ```

   or in your Docker Desktop application:

7. Now we'll create a local ECR repository to store our Docker image. Run the following command in your terminal:

   ```bash
   $> awslocal ecr create-repository --repository-name test-ecr-repo
   ```

   The service will return a JSON object that contains a field "repositoryUri" that contains the URI of the repository we just created. Copy the URI to working memory. You are going to need it in the next step.

   Then run the following command and replace <REPOSITORY_URI> with the URI you copied in the previous step (note the period argument at the end of the command):

   ```bash
   $> docker build -t <REPOSITORY_URI> .
   ```

   After the build completes, tag your new image with the following command:

   ```bash
   $> docker tag test-ecr-repo:latest <REPOSITORY_URI>:latest
   ```

8. The last command builds our Docker image for our NGINX web server (specified in our _Dockerfile_ in the root directory). After the build is complete, we push the Docker image to the local ECR repository we created earlier. Run the following command in your terminal:

   ```bash
   $> docker push <REPOSITORY_URI>
   ```

9. Now we can deploy all our ECS task definitions, services, and tasks, which allow us to deploy our ECR containers via the ECS Fargate launch type, that leverages the local Docker engine to deploy containers locally.

To create the necessary ECS infrastructure on our local machine, we're going to use a Cloudformation template, located inside _./templates_ directory and named "ecs.infra.yml'. To deploy the template, run the following command in your terminal:

```bash
$> awslocal cloudformation create-stack --stack-name infra --template-body file://templates/ecs.infra.yml
```

10. Wait until the stack status changes to **CREATE_COMPLETE** before you go on to the next step. This one can take a while. You can check the stack satus by running the following command:

```bash
$> awslocal cloudformation wait stack-create-complete --stack-name infra
```

You can also check online via the LocalStack web console at [LocalStack dashboard](http://app.localstack.cloud/inst/default/resources) once you're signed in

11. Now we can use Cloudformation to also deploy our ECS service. We will use a different file for this, also located inside the ./templates directory and named "ecs.service.yml". This template will deploy the ECS service on AWS Fargate and expose it via a public load balancer. To deploy the template, run the following command in your terminal:

```bash
$> awslocal cloudformation create-stack --stack-name ecs --template-body file://templates/ecs.service.yml -parameters ParameterKey=ImageUrl,ParameterValue=<REPOSITORY_URI>
```

### Backend Development

### Database Management

The Lead Billing Engine uses PostgreSQL as its database. The database is managed using SQLAlchemy ORM, which provides a high-level interface for interacting with the database.

We used DB Diagram to design the database schema. You can view the schema [here](https://dbdiagram.io/d/Material-Bank-Lead-Billing-Engine-67d3b5dd75d75cc8440caad6). In the diagram, you can see the relationships between the different tables in the database. Although we receive the data in JSON format inside a large object, we store it in a relational database across several tables for better performance and scalability.

We designed the schema to store leads that come in from different sources, such as our web site, social media, email marketing campaigns, referrals, webinars, events, referrals, demo requests, trade shows, conferences, newsletters, and feedback. Each lead is associated with a specific product, and we store the product information in a separate table. We also receive _multiple_ actions for each lead

### Deployment Automation
