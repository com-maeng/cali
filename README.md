# cali

> [!NOTE]
> 서예인을 위한 AI 자전 앱

### 개발 환경 구축

애플리케이션 개발 환경 구축을 위해 Docker Compose를 사용할 수 있습니다.  
아래는 환경을 구축하기 위한 커맨드의 예시입니다.

```bash
docker compose --env-file .env.dev build --no-cache  # 개발 환경에서 사용할 .env 파일의 경로를 설정
docker compose --env-file .env.dev up -d
```
