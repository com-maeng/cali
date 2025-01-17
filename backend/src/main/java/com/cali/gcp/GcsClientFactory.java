package com.cali.gcp;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;

import java.io.IOException;
import java.io.InputStream;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GcsClientFactory {

    @Bean
    public Storage GcsClient() throws IOException {
        String keyFileName = System.getenv("SERVICE_ACCOUNT_KEY_NAME");
        if (keyFileName == null || keyFileName.isEmpty()) {
            throw new RuntimeException("Environment variable SERVICE_ACCOUNT_KEY_NAME is not set or empty");
        }

        InputStream credentialsStream = GcsClientFactory.class.getResourceAsStream("/" + keyFileName + ".json");
        if (credentialsStream == null) {
            throw new RuntimeException("Service account key not found in classpath: " + keyFileName);
        }

        GoogleCredentials credentials = GoogleCredentials.fromStream(credentialsStream);
        return StorageOptions.newBuilder()
                .setCredentials(credentials)
                .build()
                .getService();
    }
}
