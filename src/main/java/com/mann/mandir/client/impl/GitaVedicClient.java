package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
public class GitaVedicClient extends BaseApiClient {

    private final ApiProperties apiProps;
    private final ObjectMapper objectMapper;

    GitaVedicClient(WebClient.Builder builder, ApiProperties apiProps, ObjectMapper objectMapper,
                    @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                    @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
        this.objectMapper = objectMapper;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getGita().getVedic().getBaseUrl();
    }

    public Optional<VedicVerseResponse> getSlok(int chapter, int verse) {
        return get("/slok/" + chapter + "/" + verse, VedicVerseResponse.class);
    }

    public Optional<List<VedicChapterResponse>> getAllChapters() {
        try {
            byte[] bytes = client()
                    .get()
                    .uri("/chapters")
                    .retrieve()
                    .bodyToMono(byte[].class)
                    .block();
            if (bytes == null || bytes.length == 0) return Optional.empty();
            List<VedicChapterResponse> chapters = objectMapper.readValue(bytes, new TypeReference<>() {});
            return Optional.ofNullable(chapters);
        } catch (Exception e) {
            log.error("Error calling {}{}: {}", getBaseUrl(), "/chapters", e.getMessage());
            return Optional.empty();
        }
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class VedicVerseResponse {
        private String slok;
        private String transliteration;
        private Map<String, Object> tej;
        private Map<String, Object> siva;
        private Map<String, Object> purohit;
        private Map<String, Object> chinmay;
        private Map<String, Object> san;
        private Map<String, Object> adi;
        private Map<String, Object> gambir;
        private Map<String, Object> madhav;
        private Map<String, Object> anand;
        private Map<String, Object> rams;
        private Map<String, Object> ramsuk;
        private Map<String, Object> hari;
        private Map<String, Object> ms;
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class VedicChapterResponse {
        private int chapter_number;
        private String name;
        private String translation;
        private int verses_count;
    }
}
