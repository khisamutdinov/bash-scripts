FROM ubuntu:latest

LABEL org.opencontainers.image.source https://github.com/khisamutdinov/bash-scripts
RUN \
    apt-get update && \ 
    apt-get install -y wget && \
    OCT_V=0.16.1 && \
    wget https://github.com/vmware-tanzu/octant/releases/download/v${OCT_V}/octant_${OCT_V}_Linux-64bit.tar.gz -O octant.tar.gz && \
    tar -xzvf octant.tar.gz

CMD OCTANT_LISTENER_ADDR=0.0.0.0:7777 octant_${OCT_V}_Linux-64bit/octant --kubeconfig /kube/config --disable-open-browser