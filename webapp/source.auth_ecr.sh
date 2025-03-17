#!/bin/bash

# source source.auth-ecr.sh ${AWS_PROFILE}
AWS_PROFILE_HERE=$1 # prevent override of AWS_PROFILE
[ -z ${AWS_PROFILE_HERE} ] && echo "AWS_PROFILE_HERE is required" && return 1
AWS_ACCOUNT=$(aws sts get-caller-identity --profile ${AWS_PROFILE_HERE} | jq -r ".Account")
AWS_REGION=$(aws configure get region --profile ${AWS_PROFILE_HERE})

export DOCKER_REGISTRY=${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${DOCKER_REGISTRY}
