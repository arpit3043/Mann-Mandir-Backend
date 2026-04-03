package com.mann.mandir.service.impl;

import com.mann.mandir.constants.enums.ContentDomain;
import com.mann.mandir.dto.domain.SearchResultDto;
import com.mann.mandir.service.GodService;
import com.mann.mandir.service.ScriptureService;
import com.mann.mandir.service.SearchService;
import com.mann.mandir.service.VedaService;
import com.mann.mandir.util.PaginationUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class SearchServiceImpl implements SearchService {

    private final GodService godService;
    private final ScriptureService scriptureService;
    private final VedaService vedaService;

    @Override
    public List<SearchResultDto> search(String query, String domain, int page, int size) {
        String q = query.toLowerCase().trim();

        ContentDomain contentDomain = ContentDomain.fromString(domain);
        List<SearchResultDto> combined = new ArrayList<>();

        if (contentDomain == null || contentDomain == ContentDomain.GOD) {
            combined.addAll(searchAartis(q));
            combined.addAll(searchChalisas(q));
            combined.addAll(searchStotrams(q));
        }

        if (contentDomain == null || contentDomain == ContentDomain.SCRIPTURES) {
            combined.addAll(searchGita(q));
        }

        if (contentDomain == null || contentDomain == ContentDomain.VEDAS) {
            combined.addAll(searchVedas(q));
        }

        combined.sort(Comparator.comparingDouble(SearchResultDto::getRelevanceScore).reversed());
        return PaginationUtils.paginate(combined, page, size);
    }

    @Override
    public long count(String query, String domain) {
        return search(query, domain, 0, Integer.MAX_VALUE).size();
    }

    private List<SearchResultDto> searchAartis(String q) {
        return godService.getAartis(null, 0, 100).stream()
                .filter(a -> matches(q, a.getName(), a.getDeity()))
                .map(a -> SearchResultDto.builder()
                        .id(a.getId()).type("AARTI").source("GOD")
                        .title(a.getName())
                        .snippet(truncate(a.getTranslation(), 120))
                        .relevanceScore(score(q, a.getName(), a.getDeity()))
                        .metadata(Map.of("deity", a.getDeity()))
                        .build())
                .collect(Collectors.toList());
    }

    private List<SearchResultDto> searchChalisas(String q) {
        return godService.getChalisas(0, 50).stream()
                .filter(c -> matches(q, c.getTitle(), c.getDeity()))
                .map(c -> SearchResultDto.builder()
                        .id(c.getId()).type("CHALISA").source("GOD")
                        .title(c.getTitle())
                        .snippet(c.getDeity() + " Chalisa — " + c.getTotalVerses() + " verses")
                        .relevanceScore(score(q, c.getTitle(), c.getDeity()))
                        .metadata(Map.of("deity", c.getDeity(), "verses", c.getTotalVerses()))
                        .build())
                .collect(Collectors.toList());
    }

    private List<SearchResultDto> searchStotrams(String q) {
        return godService.getStotrams(null, 0, 100).stream()
                .filter(s -> matches(q, s.getName(), s.getDeity(), s.getDescription()))
                .map(s -> SearchResultDto.builder()
                        .id(s.getId()).type("STOTRAM").source("GOD")
                        .title(s.getName())
                        .snippet(truncate(s.getDescription(), 120))
                        .relevanceScore(score(q, s.getName(), s.getDeity()))
                        .metadata(Map.of("deity", s.getDeity(), "author", Optional.ofNullable(s.getAuthor()).orElse("")))
                        .build())
                .collect(Collectors.toList());
    }

    private List<SearchResultDto> searchGita(String q) {
        return scriptureService.getGitaChapters().stream()
                .filter(c -> matches(q, c.getName(), c.getTranslation(), c.getSummary()))
                .map(c -> SearchResultDto.builder()
                        .id("gita_ch_" + c.getNumber()).type("CHAPTER").source("BHAGAVAD_GITA")
                        .title("Chapter " + c.getNumber() + " — " + c.getTranslation())
                        .snippet(truncate(c.getSummary(), 120))
                        .relevanceScore(score(q, c.getName(), c.getTranslation()))
                        .metadata(Map.of("chapter", c.getNumber(), "verses", c.getVersesCount()))
                        .build())
                .collect(Collectors.toList());
    }

    private List<SearchResultDto> searchVedas(String q) {
        return vedaService.getAllVedas().stream()
                .filter(v -> matches(q, v.getName(), v.getDescription()))
                .map(v -> SearchResultDto.builder()
                        .id(v.getVedaId()).type("VEDA").source("VEDA")
                        .title(v.getName())
                        .snippet(truncate(v.getDescription(), 120))
                        .relevanceScore(score(q, v.getName(), v.getDescription()))
                        .metadata(Map.of("hymns", v.getHymns(), "verses", v.getVerses()))
                        .build())
                .collect(Collectors.toList());
    }

    private boolean matches(String query, String... fields) {
        return Arrays.stream(fields)
                .filter(Objects::nonNull)
                .anyMatch(f -> f.toLowerCase().contains(query));
    }

    private double score(String query, String... fields) {
        return Arrays.stream(fields)
                .filter(Objects::nonNull)
                .mapToDouble(f -> {
                    String lower = f.toLowerCase();
                    if (lower.equals(query)) {
                        return 1.0;
                    }
                    if (lower.startsWith(query)) {
                        return 0.9;
                    }
                    if (lower.contains(query)) {
                        return 0.7;
                    }
                    return 0.0;
                }).max().orElse(0.0);
    }

    private String truncate(String text, int max) {
        if (text == null) {
            return "";
        }
        return text.length() <= max
                ? text : text.substring(0, max) + "…";
    }
}
