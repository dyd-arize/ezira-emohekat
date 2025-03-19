#!/bin/bash
shopt -s expand_aliases

alias k='kubectl'
k -n webapp create secret generic postgres-secrets --from-env-file=./postgres/postgres.env
k -n webapp create secret generic webapp-secrets --from-env-file=./webapp/webapp.env
k -n webapp create secret generic minio-secrets --from-env-file=./minio/minio.env
k -n webapp create secret generic rabbitmq-secrets --from-env-file=./decouple/rabbitmq.env
k -n webapp create secret generic celery-secrets --from-env-file=./decouple/celery.env

# would be nice to have a helm chart
k -n webapp apply \
    -f ./postgres/postgres.yaml \
    -f ./webapp/webapp.yaml \
    -f ./minio/minio.yaml \
    -f ./decouple/

k -n webapp get pods
