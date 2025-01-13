package com.cali.service;

import java.util.List;

import org.springframework.http.ResponseEntity;

public interface SearchService {

    public List<String> getSearchResult(String query);

    public ResponseEntity<String> getHanjaImage(String query, String style);

}
