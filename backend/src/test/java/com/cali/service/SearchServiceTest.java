package com.cali.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

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
        String query = "청";
        List<String> expectedResult = new ArrayList<String>() {
            {
                add("푸를 청 靑");
                add("맑을 청 淸");
                add("청할 청 請");
                add("들을 청 聽");
                add("관청 청 廳");
            }
        };
        ArrayList<HashMap<String, Object>> searchResult = new ArrayList<>();
        HashMap<String, Object> hit1 = new HashMap<>();
        hit1.put("hanja_id", "1");
        hit1.put("hanja_hun_eum", "푸를 청 靑");
        searchResult.add(hit1);
        HashMap<String, Object> hit2 = new HashMap<>();
        hit2.put("hanja_id", "2");
        hit2.put("hanja_hun_eum", "맑을 청 淸");
        searchResult.add(hit2);
        HashMap<String, Object> hit3 = new HashMap<>();
        hit3.put("hanja_id", "3");
        hit3.put("hanja_hun_eum", "청할 청 請");
        searchResult.add(hit3);
        HashMap<String, Object> hit4 = new HashMap<>();
        hit4.put("hanja_id", "4");
        hit4.put("hanja_hun_eum", "들을 청 聽");
        searchResult.add(hit4);
        HashMap<String, Object> hit5 = new HashMap<>();
        hit5.put("hanja_id", "5");
        hit5.put("hanja_hun_eum", "관청 청 廳");
        searchResult.add(hit5);

        Mockito.when(meilisearchService.search(query)).thenReturn(searchResult);

        // When
        List<String> response = searchService.getSearchResult(query);

        // Then
        Assertions.assertEquals(expectedResult, response);
        Mockito.verify(meilisearchService).search(query);
    }
}
