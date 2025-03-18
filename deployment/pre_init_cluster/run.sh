#!/bin/bash
set -a && source .env && set +a
# bash ./scripts/cert_manager.sh
bash ./scripts/lb_controller.sh
# bash ./scripts/ingress_controller.sh
bash ./scripts/core_dns.sh
