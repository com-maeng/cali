package com.cali.service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.cali.gcp.GcsService;
import com.cali.meilisearch.MeilisearchService;
import com.cali.repository.ImageResponse;
import com.meilisearch.sdk.exceptions.MeilisearchApiException;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SearchServiceImpl implements SearchService {

    private final MeilisearchService meilisearchService;
    private final GcsService gcsService;

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

    @Override
    public List<ImageResponse> getHanjaImages(String query, String style) {
        String bucketName = System.getenv("HANJA_BUCKET");

        String[] parts = query.split(" ");
        String folderPath = parts[1] + "/" + parts[2] + "/" + style;

        return gcsService.getImages(bucketName, folderPath);
    }

}
