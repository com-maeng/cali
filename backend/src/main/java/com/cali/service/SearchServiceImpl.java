package com.cali.service;

import org.springframework.stereotype.Service;

import com.cali.meilisearch.MeilisearchService;
import com.meilisearch.sdk.exceptions.MeilisearchApiException;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SearchServiceImpl implements SearchService {

    private final MeilisearchService meilisearchService;

    @Override
    public String getSearchResult(String query) {

        String searchResult = "";

        try {
            searchResult = meilisearchService.search(query).get(0).get("title").toString();
        } catch (MeilisearchApiException e) {
            searchResult = "search API Exception";
        }
        return searchResult;
    }
}
