package com.cali.service;

import java.util.ArrayList;
import java.util.Arrays;
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
    public List<ImageResponse> getHanjaImages(String query, String style, int offset) {
        int checkHun = query.split(" ").length;
        String[] parts = query.split(" ");
        String folderPath = "";
        if (checkHun <= 3) {
            folderPath = parts[1] + "/" + parts[2] + "/" + style;
        } else {
            folderPath = Arrays.stream(parts, 1, parts.length - 1)
                    .collect(Collectors.joining(" "))
                    .trim()
                    + "/" + parts[parts.length - 1] + "/" + style;
        }
        if (checkFolderPath(folderPath)) {
            throw new RuntimeException("The folderPath character structure is not valid: " + folderPath);
        }
        return gcsService.getImages(folderPath, offset);
    }

    public boolean checkFolderPath(String folderPath) {
        int totalLength = folderPath.length();
        int checkLength = folderPath.replace("/", "").length();
        if ((totalLength - checkLength) == 2) {
            return false;
        }
        return true;
    }

}
