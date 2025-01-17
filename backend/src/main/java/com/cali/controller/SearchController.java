package com.cali.controller;

import org.springframework.web.bind.annotation.RestController;

import com.cali.service.SearchServiceImpl;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import lombok.RequiredArgsConstructor;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1")
@Validated
public class SearchController {

    private final SearchServiceImpl searchService;

    @GetMapping("/search")
    public List<String> getSearchResult(@RequestParam(value = "q") String query) {
        return searchService.getSearchResult(query);
    }

    @GetMapping(value = "/images")
    public ResponseEntity<?> getHanjaImages(@Valid @RequestParam(value = "q") @NotBlank String query,
            @Valid @RequestParam(value = "s") @NotBlank String style) {
        return ResponseEntity.ok().body(searchService.getHanjaImages(query, style));
    }

}
