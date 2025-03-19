#!/bin/bash
set -euo pipefail
echo "::INFO:: Installing Metrics Server"
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ --force-update
helm upgrade --install metrics-server metrics-server/metrics-server --namespace kube-system
