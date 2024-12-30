package com.cali.meilisearch;

import com.meilisearch.sdk.Client;
import com.meilisearch.sdk.Config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MeilisearchClientFactory {

    @Bean
    public Client MeilisearchClient() {
        String host = System.getenv().getOrDefault("MEILI_HOST", "http://localhost:7700");
        String apiKey = System.getenv().getOrDefault("MEILI_MASTER_KEY", "masterKey");

        // Meilisearch 클라이언트를 생성하여 반환합니다.
        return new Client(new Config(host, apiKey));
    }
}
