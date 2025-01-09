package com.cali.controller;

import org.springframework.web.bind.annotation.RestController;

import com.cali.gcp.GcsClient;
import com.cali.service.SearchServiceImpl;

import lombok.RequiredArgsConstructor;

import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.Storage;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
public class SearchController {

    private final SearchServiceImpl searchService;

    @GetMapping("/search")
    public List<String> getSearchResult(@RequestParam(value = "q") String query) {
        return searchService.getSearchResult(query);
    }

    @GetMapping(value = "/image", produces = "image/webp")
    public byte[] getHanjaImage() throws Exception {
        String bucketName = System.getenv("HANJA_BUCKET");
        String objectName = "고리/환/-_사신비_2024-12-29T16:13:52.450855+09:00.webp";

        Storage storage = GcsClient.getGcsStorage();
        Blob blob = storage.get(bucketName, objectName);
        if (blob == null) {
            throw new RuntimeException("Object not found: " + objectName);
        }

        return blob.getContent();
    }

    // sample
    /**
     * 특정 경로의 모든 이미지를 반환 (바이트 배열 목록)
     *
     * @param bucketName GCS 버킷 이름
     * @param folderPath 이미지 경로 (예: "고리/")
     * @return 이미지 파일 목록
     */
    @GetMapping(value = "/images")
    public ResponseEntity<String> getImagesAsHtml(@RequestParam(value = "qi") String folderPath) throws Exception {
        String bucketName = System.getenv("HANJA_BUCKET");
        Storage storage = GcsClient.getGcsStorage();

        Iterable<Blob> blobs = storage.list(bucketName).iterateAll();
        List<String> imageTags = new ArrayList<>();

        for (Blob blob : blobs) {
            if (blob.getName().startsWith(folderPath) && isImage(blob.getName())) {
                byte[] imageBytes = blob.getContent();
                String base64Image = Base64.getEncoder().encodeToString(imageBytes);
                imageTags.add("<img src='data:image/jpeg;base64," + base64Image + "' alt='" + blob.getName() + "'/>");
            }
        }

        if (imageTags.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        String htmlResponse = "<html><body>" + String.join("<br/>", imageTags) + "</body></html>";
        return ResponseEntity.ok().body(htmlResponse);
    }

    /**
     * 이미지 파일인지 확인 (확장자 기반)
     *
     * @param fileName 파일 이름
     * @return 이미지 여부
     */
    private boolean isImage(String fileName) {
        String lowerName = fileName.toLowerCase();
        return lowerName.endsWith(".jpg") || lowerName.endsWith(".jpeg") ||
                lowerName.endsWith(".png") || lowerName.endsWith(".webp");
    }

}
