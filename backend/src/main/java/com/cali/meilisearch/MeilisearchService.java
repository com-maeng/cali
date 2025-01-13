package com.cali.meilisearch;

import java.util.ArrayList;
import java.util.HashMap;

import org.springframework.stereotype.Service;

import com.meilisearch.sdk.Client;
import com.meilisearch.sdk.Index;
import com.meilisearch.sdk.SearchRequest;
import com.meilisearch.sdk.exceptions.MeilisearchApiException;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class MeilisearchService {

    private final Client meilisearchClient;

    public ArrayList<HashMap<String, Object>> search(String query) throws MeilisearchApiException {
        Index index = meilisearchClient.getIndex("hanja");
        return index.search(new SearchRequest(query)
                .setLimit(5)).getHits();
    }
}
