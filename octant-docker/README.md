# Octant docker image

## Run locally 
Prerequisits - kubectl should be installed, kube configuration is set up to be at ~/.kube/config
```
$ docker-compose up -d
```
or
```
$ docker run -d -v ~/.kube/config:/kube/config:ro -p 7777:7777 khisamutdinov/octant:latest
```
After this just go to http://localhost:7777