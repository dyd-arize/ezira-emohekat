#!/bin/bash

# handle source vs bash, prevent killing the shell
if [ -z ${AWS_PROFILE} ]; then
    echo "AWS_PROFILE is required"
    if [ $0 != "$BASH_SOURCE" ]; then
        return 1
    else
        exit 1
    fi
fi

AWS_ACCOUNT=$(aws sts get-caller-identity | jq -r ".Account")
AWS_REGION=$(aws configure get region)

export DOCKER_REGISTRY=${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}
