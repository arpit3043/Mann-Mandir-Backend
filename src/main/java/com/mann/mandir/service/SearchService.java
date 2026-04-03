package com.mann.mandir.service;

import com.mann.mandir.dto.domain.SearchResultDto;

import java.util.List;

public interface SearchService {
    List<SearchResultDto> search(String query, String domain, int page, int size);
    long count(String query, String domain);
}
