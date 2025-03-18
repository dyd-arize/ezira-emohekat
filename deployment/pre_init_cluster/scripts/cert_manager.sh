# #!/bin/bash
# # https://cert-manager.io/docs/installation/helm/
# set -euo pipefail
# echo "Installing cert-manager..."
# helm repo add jetstack https://charts.jetstack.io --force-update
# helm upgrade --install \
#   cert-manager jetstack/cert-manager \
#   --namespace cert-manager \
#   --create-namespace \
#   --version v1.17.0 \
#   --set crds.enabled=true
