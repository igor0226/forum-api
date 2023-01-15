#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "Error: please pass app version"
    exit 1
fi

cd frontend
docker build -t app-frontend:$1 -f ./Dockerfile.prod .
docker tag app-frontend:$1 cr.yandex/crpli9f3ae0v1b2slej3/app-frontend:latest
docker push cr.yandex/crpli9f3ae0v1b2slej3/app-frontend:latest
