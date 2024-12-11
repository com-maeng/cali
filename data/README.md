## How To Run

배치 데이터 파이프라인 컨테이너 실행 시에 .env 파일과 GCP Service Acount Key의 경로를 명시해주어야 합니다.

```bash
# 컨테이너 실행 예시 커맨드
docker run --env-file .env.prod \
    --volume ./gcp_service_account_key_file.json:/cali/gcp_service_account_key_file.json \
    pipeline-image:latest
```
