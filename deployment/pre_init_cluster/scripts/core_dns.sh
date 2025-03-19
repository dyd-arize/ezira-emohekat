#!/bin/bash
set -euo pipefail
echo "::INFO:: Installing CoreDNS"
helm repo add coredns https://coredns.github.io/helm --force-update
helm --namespace=kube-system install coredns coredns/coredns
