package com.cali.service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.cali.meilisearch.MeilisearchService;
import com.meilisearch.sdk.exceptions.MeilisearchApiException;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SearchServiceImpl implements SearchService {

    private final MeilisearchService meilisearchService;

    @Override
    public List<String> getSearchResult(String query) {

        List<String> searchResult = new ArrayList<String>();
        try {
            searchResult = meilisearchService.search(query).stream()
                    .map(result -> result.get("hanja_hun_eum").toString())
                    .collect(Collectors.toList());
        } catch (MeilisearchApiException e) {
            System.err.printf("meilisearch api exception!\n%s", e.toString());
        }
        return searchResult;
    }
}
