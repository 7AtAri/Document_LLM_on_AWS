# LLM Document Analysis with AWS

## AWS Technologies used

- ECR (Elastic Cloud Repository) for docker containers
- S3
- Fargate (for deployment of containers)

## Other Modules used

- Langchain
- Faiss

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

- set up an S3 bucket for the project and upload the model to it
- set up ECS Fargate with proper compute and the docker image-URI
