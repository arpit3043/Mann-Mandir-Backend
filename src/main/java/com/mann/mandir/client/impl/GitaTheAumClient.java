package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.mann.mandir.client.BaseApiClient;
import com.mann.mandir.config.ApiProperties;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Slf4j
@Component
public class GitaTheAumClient extends BaseApiClient {

    private final ApiProperties apiProps;
    private final ObjectMapper objectMapper;

    GitaTheAumClient(WebClient.Builder builder, ApiProperties apiProps, ObjectMapper objectMapper,
                     @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                     @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
        this.objectMapper = objectMapper;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getGita().getTheaum().getBaseUrl();
    }

    public Optional<TheAumVerseResponse> getVerse(int chapter, int verse) {
        return get("/text/" + chapter + "/" + verse, TheAumVerseResponse.class);
    }

    public Optional<List<TheAumVerseResponse>> getChapterVerses(int chapter) {
        return get("/text/" + chapter, new ParameterizedTypeReference<>() {});
    }

    public Optional<TheAumChapterResponse> getChapter(int chapter) {
        return get("/chapter/" + chapter, TheAumChapterResponse.class);
    }

    public Optional<List<TheAumChapterResponse>> getAllChapters() {
        try {
            byte[] bytes = client()
                    .get()
                    .uri("/chapters/")
                    .retrieve()
                    .bodyToMono(byte[].class)
                    .block();
            if (bytes == null || bytes.length == 0) return Optional.empty();
            List<TheAumChapterResponse> chapters = objectMapper.readValue(bytes, new TypeReference<>() {});
            return Optional.ofNullable(chapters);
        } catch (Exception e) {
            log.error("Error calling {}{}: {}", getBaseUrl(), "/chapters/", e.getMessage());
            return Optional.empty();
        }
    }

    public Optional<TheAumTranslationResponse> getVerseTranslations(int chapter, int verse) {
        return get("/text/translations/" + chapter + "/" + verse, TheAumTranslationResponse.class);
    }

    public Optional<TheAumTransliterationResponse> getVerseTransliteration(int chapter, int verse) {
        return get("/text/transliterations/" + chapter + "/" + verse, TheAumTransliterationResponse.class);
    }

    public Optional<TheAumCommentaryResponse> getVerseCommentary(int chapter, int verse) {
        return get("/text/commentaries/" + chapter + "/" + verse, TheAumCommentaryResponse.class);
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TheAumVerseResponse {
        @JsonProperty("bg_id") private String bgId;
        private int chapter;
        private int verse;
        private String shloka;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TheAumChapterResponse {
        @JsonProperty("chapter_number") private int number;
        private String name;
        private String translation;
        private String transliteration;
        @JsonProperty("verses_count") private int versesCount;
        private Object summary;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TheAumTranslationResponse {
        private Map<String, String> translations;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TheAumTransliterationResponse {
        private String transliteration;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class TheAumCommentaryResponse {
        private Map<String, String> commentaries;
    }
}
