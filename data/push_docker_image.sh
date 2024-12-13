#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: 스크립트 실행 시 Dotenv 파일을 인자로 제공해야 합니다."
  exit 1
fi


if [ ! -f "$1" ]; then
  echo "Error: Dotenv 파일 '$FILE'가 존재하지 않거나 비정상적인 파일입니다."
  exit 1
fi

source "$1"

ARTIFACT_REGISTRY_URL=$ARTIFACT_REGISTRY_REGION/$GCP_PROJECT_ID/$ARTIFACT_REGISTRY_REPOSITORY

# Login
cat $SECRETS_DIR/$SERVICE_ACCOUNT_KEY_NAME.json | \
    docker login -u _json_key --password-stdin $ARTIFACT_REGISTRY_URL

# Build
docker build \
  --no-cache \
  --platform linux/amd64 \
  -t $ARTIFACT_REGISTRY_URL/$ARTWORK_DATA_PIPELINE_IMAGE_NAME \
  data

# Push
docker push $ARTIFACT_REGISTRY_URL/$ARTWORK_DATA_PIPELINE_IMAGE_NAME
