package com.cali;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import com.cali.meilisearch.MeilisearchConfig;

@SpringBootTest
class CaliApplicationTests {

	@MockitoBean
	private MeilisearchConfig sMeilisearchConfig;

	@Test
	void contextLoads() {
	}

}
