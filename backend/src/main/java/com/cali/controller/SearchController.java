package com.cali.controller;

import org.springframework.web.bind.annotation.RestController;

import com.cali.repository.ImageResponse;
import com.cali.service.SearchServiceImpl;

import lombok.RequiredArgsConstructor;

import java.util.List;

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

    @GetMapping(value = "/images")
    public ResponseEntity<List<ImageResponse>> getHanjaImages(@RequestParam(value = "q") String query,
            @RequestParam(value = "s") String style) {
        return ResponseEntity.ok().body(searchService.getHanjaImages(query, style));
    }

}
