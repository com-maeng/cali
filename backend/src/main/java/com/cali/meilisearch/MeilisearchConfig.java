package com.cali.meilisearch;

import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.context.annotation.Configuration;

import com.meilisearch.sdk.Client;
import com.meilisearch.sdk.Index;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;

@Configuration
@RequiredArgsConstructor
public class MeilisearchConfig {

    private final Client meilisearchClient;

    @PostConstruct
    public void init() {
        String dummyData = createDummyData();
        addDocuments(dummyData);
    }

    private String createDummyData() {
        // Dummy Data
        JSONArray array = new JSONArray();
        ArrayList<JSONObject> items = new ArrayList<JSONObject>() {
            {
                add(new JSONObject().put("id", "1").put("title", "Carol").put("genres",
                        new JSONArray("[\"Romance\",\"Drama\"]")));
                add(new JSONObject().put("id", "2").put("title", "Wonder Woman").put("genres",
                        new JSONArray("[\"Action\",\"Adventure\"]")));
                add(new JSONObject().put("id", "3").put("title", "Life of Pi").put("genres",
                        new JSONArray("[\"Adventure\",\"Drama\"]")));
                add(new JSONObject().put("id", "4").put("title", "Mad Max: Fury Road").put("genres",
                        new JSONArray("[\"Adventure\",\"Science Fiction\"]")));
                add(new JSONObject().put("id", "5").put("title", "Moana").put("genres",
                        new JSONArray("[\"Fantasy\",\"Action\"]")));
                add(new JSONObject().put("id", "6").put("title", "Philadelphia").put("genres",
                        new JSONArray("[\"Drama\"]")));
            }
        };

        array.put(items);
        return array.getJSONArray(0).toString();

    }

    private void addDocuments(String docJson) {
        Index index = meilisearchClient.index("chi");
        index.addDocuments(docJson);
    }
}
