helm repo add coredns https://coredns.github.io/helm --force-update
helm --namespace=kube-system install coredns coredns/coredns
