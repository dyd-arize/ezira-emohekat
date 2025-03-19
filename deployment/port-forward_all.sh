#/bin/bash
shopt -s expand_aliases

alias k='kubectl'
k -n webapp port-forward service/postgres 5432 > /dev/null 2>&1 &
k -n webapp port-forward service/webapp 5000 > /dev/null 2>&1 &
k -n webapp port-forward service/minio 9001 > /dev/null 2>&1 &
k -n webapp port-forward service/cflower 5555 > /dev/null 2>&1 &
