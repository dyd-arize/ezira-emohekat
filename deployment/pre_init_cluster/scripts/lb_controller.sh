#!/bin/bash
# https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
[ -z $CLUSTER_NAME ] && echo '$CLUSTER_NAME is required' && exit 1

echo "Installing AWS Load Balancer Controller..."

POLICY_NAME="AWSLoadBalancerControllerIAMPolicy"
SERVICE_ACCOUNT_NAME="aws-load-balancer-controller"
POLICY_ARN=$(aws iam list-policies --scope Local --query "Policies[?PolicyName=='${POLICY_NAME}'].Arn" --output text)
if [ -z $POLICY_ARN ]; then
  echo "Creating ${POLICY_NAME}..."
  aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://$SCRIPT_DIR/lb_controller_iam_policy.json
else
  echo "${POLICY_NAME} already exists. Skipping..."
fi

eksctl utils associate-iam-oidc-provider --region=us-west-1 --cluster=$CLUSTER_NAME --approve
eksctl create iamserviceaccount \
  --cluster=$CLUSTER_NAME \
  --namespace=kube-system \
  --name=$SERVICE_ACCOUNT_NAME \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::$(aws sts get-caller-identity | jq -r ".Account"):policy/$POLICY_NAME \
  --approve

helm repo add eks https://aws.github.io/eks-charts --force-update
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=$CLUSTER_NAME \
  --set serviceAccount.create=false \
  --set serviceAccount.name=$SERVICE_ACCOUNT_NAME \
  --set version=v2.12.0
