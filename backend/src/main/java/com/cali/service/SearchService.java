package com.cali.service;

import java.util.List;

import com.cali.repository.ImageResponse;

public interface SearchService {

    public List<String> getSearchResult(String query);

    public List<ImageResponse> getHanjaImages(String query, String style, int offset);

}
