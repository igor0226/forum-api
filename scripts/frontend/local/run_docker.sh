#!/bin/sh
cd frontend
docker run -p 8080:8080 --network='host' app-frontend
