FROM azul/zulu-openjdk-alpine:21-latest

ARG JAR_FILE=build/libs/*.jar

COPY ${JAR_FILE} cali.jar

CMD apt-get update -y

ENTRYPOINT ["java", "-jar", "/cali.jar"]
