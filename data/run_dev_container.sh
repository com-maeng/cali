#!/bin/bash

docker build --no-cache -t cali-data-dev -f ./data/Dockerfile.dev ./data

docker run -it \
    --env-file ./.env.dev \
    --volume ./keys/service_account_key_dev.json:/cali/keys/service_account_key_dev.json:ro \
    --volume ./data:/cali/data \
    cali-data-dev
