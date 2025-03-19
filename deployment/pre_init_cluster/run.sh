#!/bin/bash
set -a && source .env && set +a
# required
bash ./scripts/core_dns.sh

# optional
bash ./scripts/metrics_server.sh
bash ./scripts/cert_manager.sh
# bash ./scripts/lb_controller.sh
# bash ./scripts/ingress_controller.sh

kubectl apply -f ./manifests/

echo "::INFO:: Creating namespace webapp"
kubectl create ns webapp
