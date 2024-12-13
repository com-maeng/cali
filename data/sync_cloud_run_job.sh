#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: 스크립트 실행 시 Dotenv 파일을 인자로 제공해야 합니다."
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: Dotenv 파일 '$1'가 존재하지 않거나 비정상적인 파일입니다."
  exit 1
fi

source "$1"

JOB_NAME=$ARTWORK_DATA_PIPELINE_IMAGE_NAME-job
ARTIFACT_REGISTRY_URL=$ARTIFACT_REGISTRY_REGION/$GCP_PROJECT_ID/$ARTIFACT_REGISTRY_REPOSITORY

python data/utils/parser.py "$1"  # Get YAML version of dotenv file

if gcloud beta run jobs describe $JOB_NAME --region $GCP_DEFAULT_REGION; then
    gcloud beta run jobs update $JOB_NAME \
        --image $ARTIFACT_REGISTRY_URL/$ARTWORK_DATA_PIPELINE_IMAGE_NAME \
        --region $GCP_DEFAULT_REGION \
        --env-vars-file "$1".yaml \
        --set-secrets /cali/$SECRETS_DIR/$SERVICE_ACCOUNT_KEY_NAME.json=$SECRET_MANAGER_SERVICE_ACCOUNT_KEY
else
  gcloud beta run jobs create $JOB_NAME \
      --image $ARTIFACT_REGISTRY_URL/$ARTWORK_DATA_PIPELINE_IMAGE_NAME \
      --region $GCP_DEFAULT_REGION \
      --env-vars-file "$1".yaml \
      --set-secrets /cali/$SECRETS_DIR/$SERVICE_ACCOUNT_KEY_NAME.json=$SECRET_MANAGER_SERVICE_ACCOUNT_KEY
fi
