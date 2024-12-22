FROM azul/zulu-openjdk-alpine:21-latest

WORKDIR /backend

COPY gradle/wrapper/ gradle/wrapper/
COPY gradlew settings.gradle build.gradle ./

RUN chmod +x ./gradlew

CMD ["./gradlew", "bootRun", "--no-daemon"]
