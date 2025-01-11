package com.cali.service;

import java.util.List;

public interface SearchService {

    public List<String> getSearchResult(String query);

    public byte[] getHanjaImage(String query, String style);
}
