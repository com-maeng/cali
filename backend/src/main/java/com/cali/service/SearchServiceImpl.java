package com.cali.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.cali.gcp.GcsClient;
import com.cali.meilisearch.MeilisearchService;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.Storage;
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

    @Override
    public byte[] getHanjaImage(String query, String style) {
        String bucketName = System.getenv("HANJA_BUCKET");
        // query: 環 고리 환
        String[] parts = query.split(" ");
        String extractedPart = parts[1] + "/" + parts[2];
        String fileName = "/-_사신비_2024-12-29T16_13_52.450855+09_00.webp";
        String objectName = extractedPart + "/" + style + fileName;

        byte[] hanjaImage = new byte[] {};
        try {
            Storage storage = GcsClient.getGcsStorage();
            Blob blob = storage.get(bucketName, objectName);
            if (blob == null) {
                throw new RuntimeException("Object not found: " + objectName);
            }

            hanjaImage = blob.getContent();
        } catch (IOException e) {
            System.err.printf("GCS bucket api exception!\n%s", e.toString());
        }
        return hanjaImage;
    }
}
