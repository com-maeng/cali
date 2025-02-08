#!/bin/bash

git pull origin main

docker build -t cali-web-prototype .
docker container rm -f $(docker container ls -aq)
docker run -p 3000:3000 cali-web-prototype
