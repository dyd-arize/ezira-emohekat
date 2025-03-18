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
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
