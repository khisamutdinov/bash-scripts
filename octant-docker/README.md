# Octant docker image

## Run locally 
Prerequisits - kubectl should be installed, kube configuration is set up to be at ~/.kube/config
```
$ docker-compose up -d
```
or
```
$ docker run -d -v ~/.kube/config:/kube/config:ro -p 7777:7777 ghcr.io/khisamutdinov/octant:latest
```
After this just go to http://localhost:7777
To ease the following line could be added to ~/.bash-profile (or .zhrc if the zsh is used)
```
octant() { docker run -d -v ~/.kube/config:/kube/config:ro -p 7777:7777 ghcr.io/khisamutdinov/octant:latest }
```
After this just call
```
$ octant
``` 
