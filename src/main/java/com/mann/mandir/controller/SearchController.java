package com.mann.mandir.controller;


import com.mann.mandir.constants.RestEndpointConstants;
import com.mann.mandir.dto.ApiResponse;
import com.mann.mandir.dto.domain.SearchResultDto;
import com.mann.mandir.service.SearchService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(RestEndpointConstants.SEARCH)
@RequiredArgsConstructor
@Tag(name = "Search", description = "Cross-domain search across all Hindu content")
public class SearchController {

    private final SearchService searchService;

    @GetMapping
    @Operation(summary = "Search across all content", description = "Full-text search across Aartis, Chalisas, Stotrams, Gita, Ramayana, Mahabharata, Vedas")
    public ResponseEntity<ApiResponse<List<SearchResultDto>>>
    search(@RequestParam String query,
           @RequestParam(required = false) String domain,
           @RequestParam(defaultValue = "0") int page,
           @RequestParam(defaultValue = "20") int size) {

        List<SearchResultDto> results = searchService.search(query, domain, page, size);
        long total = searchService.count(query, domain);
        return ResponseEntity.ok(ApiResponse.ok(results, ApiResponse.PaginationMeta.of(page, size, total)));
    }
}
