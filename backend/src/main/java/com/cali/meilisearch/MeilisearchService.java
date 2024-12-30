package com.cali.meilisearch;

import java.util.ArrayList;
import java.util.HashMap;

import org.springframework.stereotype.Service;

import com.meilisearch.sdk.Client;
import com.meilisearch.sdk.Index;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class MeilisearchService {

    private final Client meilisearchClient;

    public ArrayList<HashMap<String, Object>> search(String query) {
        Index index = meilisearchClient.getIndex("chi");
        return index.search(query).getHits();
    }
}
