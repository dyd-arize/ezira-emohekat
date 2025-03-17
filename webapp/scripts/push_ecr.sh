#!/bin/bash
[ -z ${AWS_PROFILE} ] && echo "AWS_PROFILE is required" && exit 1
AWS_ACCOUNT=$(aws sts get-caller-identity | jq -r ".Account")
AWS_REGION=$(aws configure get region)

export DOCKER_REGISTRY=${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}

docker compose push web
