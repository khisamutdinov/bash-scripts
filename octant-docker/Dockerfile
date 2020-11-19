FROM ubuntu:latest

LABEL org.opencontainers.image.source https://github.com/khisamutdinov/bash-scripts
ARG octant_version
ENV octant_version=${octant_version:-0.16.1}
RUN \
    apt-get update && \ 
    apt-get install -y wget && \
    wget https://github.com/vmware-tanzu/octant/releases/download/v${octant_version}/octant_${octant_version}_Linux-64bit.tar.gz -O octant.tar.gz && \
    tar -xzvf octant.tar.gz

CMD OCTANT_LISTENER_ADDR=0.0.0.0:7777 octant_${octant_version}_Linux-64bit/octant --kubeconfig /kube/config --disable-open-browser