#!/bin/bash

NO_CACHE=""

if [ "$1" == "-n" ] || [ "$1" == "--no-cache" ]; then
    NO_CACHE="--no-cache"
fi

docker build \
    $NO_CACHE \
    -t cali-web-dev-env \
    -f Dockerfile.dev \
    .

docker run -it \
    --mount type=bind,src=./,dst=/cali/web \
    -p 127.0.0.1:3000:3000 \
    cali-web-dev-env \
    /bin/sh
