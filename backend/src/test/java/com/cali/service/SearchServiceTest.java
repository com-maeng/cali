package com.cali.service;

import java.util.ArrayList;
import java.util.HashMap;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import com.cali.meilisearch.MeilisearchService;

@ExtendWith(MockitoExtension.class)
public class SearchServiceTest {

    @Mock
    private MeilisearchService meilisearchService;
    @InjectMocks
    private SearchServiceImpl searchService;

    @Test
    void testGetSearch() {

        // Given
        String query = "pi";
        String expectedResult = "Life Of Pi";
        ArrayList<HashMap<String, Object>> searchResult = new ArrayList<>();
        HashMap<String, Object> hit = new HashMap<>();
        hit.put("id", "1");
        hit.put("title", "Life Of Pi");
        searchResult.add(hit);

        Mockito.when(meilisearchService.search(query)).thenReturn(searchResult);

        // When
        String response = searchService.getSearchResult(query);

        // Then
        Assertions.assertEquals(expectedResult, response);
        Mockito.verify(meilisearchService).search(query);
    }
}
