#!/bin/sh
cd frontend
docker build -t app-frontend -f ./Dockerfile.local .
