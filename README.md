# LLM Document Analysis with AWS

## AWS services used

- ECR (Elastic Cloud Repository) for docker containers
- S3 (for storage)
- ECS Fargate (for deployment of containers)

## framework / tools

- llamaindex (for RAG)
- Faiss ()
- Langchain (for possible future development)

## Commands

- build docker container

```bash
docker build -t aws_docker_image .
```

- giving the container a name tag that relates to the ECR (add resource in ECR first with AWS in browser):

```bash
docker tag aws_docker_image <aws_ID...amazonaws.com>
```

- after installing AWS CLI: enter the user / person access code for AWS CLI

```bash
aws config
```

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.eu-central-1.amazonaws.com
```

this should output: Login Succeeded

- then push the docker container to AWS ECR:

```bash
docker push <aws_ID...amazonaws.com>
```

- for local development build the docker with file mount:

```bash
docker run -v /path/to/local/files:mount/path <image_name>
```

- set up ECS Fargate with proper compute (1 CPU with max 5GB should be enough for the start) and the docker image-URI
- set up an S3 bucket for the project and upload the model to it
- in the IAM the ecsTaskExecutionRole needs to be selected and an AmazonS3ReadOnlyAccess permission attatched to it
- a TaskRole needs to be set up (self configured),
with AmazonS3ReadOnlyAccess permission
(this is needed for the container to get credentials for the S3 buckets)

## github action workflow

- github action workflow is set up to automate the process and start the ECS deployment of the container
- if application code changes (except for README, .dockerignore and github workflow files) the container is rebuilt and pushed to the ECR
- if anything is pushed on the github repo, this triggers the deployment of the code on AWS ECS

The new task definition within the actions workflow needs to have these parameters:

```bash
family: .family,
containerDefinitions: .containerDefinitions, 
requiresCompatibilities: ["FARGATE"], 
networkMode: "awsvpc", 
executionRoleArn: .executionRoleArn, 
taskRoleArn: .taskRoleArn, 
cpu: .cpu, 
memory: .memory
```

The following parameters that are not hardcoded need to be set
up in first in AWS ECS - Task Definitions:

- for cpu: 2vCPU are recommended
- for memory: 5GB are recommended
