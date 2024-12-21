#!/bin/sh

# Gradle build on startup
./gradlew build --no-daemon

# Start file watcher to detect changes and rebuild
while true; do
    inotifywait -r -e modify,create,delete ./src ./build.gradle ./settings.gradle ./gradle || continue
    ./gradlew build --no-daemon
done &

# Start the application
./gradlew bootRun --no-daemon
