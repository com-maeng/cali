#!/bin/bash

source .env

DOCKER_IMAGE_NAME=artwork-data-pipeline
ARTIFACT_REGISTRY_URL=$ARTIFACT_REGISTRY_REGION/$GCS_PROJECT_ID/$ARTIFACT_REGISTRY_REPOSITORY

# Login
cat service_account_key.json | \
    docker login -u _json_key --password-stdin $ARTIFACT_REGISTRY_URL

# Build
docker build -t $ARTIFACT_REGISTRY_URL/$DOCKER_IMAGE_NAME data

# Push
docker push $ARTIFACT_REGISTRY_URL/$DOCKER_IMAGE_NAME
