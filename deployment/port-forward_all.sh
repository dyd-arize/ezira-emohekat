#/bin/bash
shopt -s expand_aliases

alias k='kubectl'
k -n webapp port-forward service/postgres 5432 &2>/dev/null &
k -n webapp port-forward service/webapp 5000 &2>/dev/null &
k -n webapp port-forward service/minio 9001 &2>/dev/null &
k -n webapp port-forward service/cflower 5555 &2>/dev/null &
