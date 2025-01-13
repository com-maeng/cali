package com.cali.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
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
            System.err.printf("Meilisearch API exception!\n%s", e.toString());
        }
        return searchResult;
    }

    @Override
    public ResponseEntity<String> getHanjaImage(String query, String style) {
        List<String> images = new ArrayList<>();

        try {
            Storage storage = GcsClient.getGcsStorage();
            String bucketName = System.getenv("HANJA_BUCKET");
            // query: 環 고리 환
            String[] parts = query.split(" ");
            String folderPath = parts[1] + "/" + parts[2] + "/" + style;

            Iterable<Blob> blobs = storage.list(bucketName).iterateAll();
            for (Blob blob : blobs) {
                if (blob.getName().startsWith(folderPath) && blob.getName().endsWith(".webp")) {
                    byte[] imageBytes = blob.getContent();
                    String base64Image = Base64.getEncoder().encodeToString(imageBytes);
                    images.add("<img src='data:image/jpeg;base64," + base64Image + "' alt='" + blob.getName() + "'/>");
                }
            }
        } catch (IOException e) {
            System.err.printf("GCS bucket API exception!\n%s", e.toString());
        }

        if (images.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        }
        String htmlResponse = "<html><body>" + String.join("<br/>", images) + "</body></html>";
        return ResponseEntity.ok().body(htmlResponse);
    }

}