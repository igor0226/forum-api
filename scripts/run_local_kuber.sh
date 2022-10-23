#!/bin/sh

minikube start

./scripts/psql/build_docker.sh
./scripts/backend/build_docker.sh
./scripts/frontend/build_docker.sh

minikube image load app-psql
minikube image load app-backend
minikube image load app-frontend

kubectl apply -f deploy/

echo -n "
    Use commands below to get app endpoints:
    $ minikube service app-frontend-lb
    $ minikube service app-backend-lb
" | tail -n 3
