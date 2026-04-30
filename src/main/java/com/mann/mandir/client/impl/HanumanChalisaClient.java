package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mann.mandir.client.BaseApiClient;
import com.mann.mandir.config.ApiProperties;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Optional;
import java.util.Random;

@Slf4j
@Component
public class HanumanChalisaClient extends BaseApiClient {

    private final ApiProperties apiProps;
    private final ObjectMapper objectMapper;

    HanumanChalisaClient(WebClient.Builder builder, ApiProperties apiProps, ObjectMapper objectMapper,
                         @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                         @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
        this.objectMapper = objectMapper;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getChalisa().getHanuman().getBaseUrl();
    }

    public Optional<List<ChalisaVerseResponse>> getAllVerses() {
        try {
            String body = client()
                    .get()
                    .uri("/hanumanChalisa.json")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            if (body == null || body.isBlank()) {
                return Optional.empty();
            }

            List<ChalisaVerseResponse> verses = objectMapper.readValue(
                    body,
                    new TypeReference<List<ChalisaVerseResponse>>() {}
            );
            return Optional.ofNullable(verses);
        } catch (Exception e) {
            log.error("Error calling {}{}: {}", getBaseUrl(), "/hanumanChalisa.json", e.getMessage());
            return Optional.empty();
        }
    }

    public Optional<ChalisaVerseResponse> getVerse(int number) {
        return getAllVerses()
                .flatMap(list -> list.stream().filter(v -> v.getNumber() == number).findFirst());
    }

    public Optional<ChalisaVerseResponse> getRandomVerse() {
        return getAllVerses()
                .flatMap(list -> list.isEmpty()
                        ? Optional.empty()
                        : Optional.of(list.get(new Random().nextInt(list.size()))));
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ChalisaVerseResponse {
        @JsonProperty("id")
        private int number;
        private String type;
        @JsonProperty("verse")
        private String devanagari;
        private String transliteration;
        @JsonProperty("english_translation")
        private String englishTranslation;
        @JsonProperty("hindi_translation")
        private String hindiTranslation;
        @JsonProperty("translations")
        private List<Translation> translations;
        private String meter;
        private List<String> tags;
        private String summary;

        @Data
        @JsonIgnoreProperties(ignoreUnknown = true)
        public static class Translation {
            @JsonProperty("translation_id")
            private Integer translationId;
            @JsonProperty("translation_type")
            private String translationType;
            @JsonProperty("translation")
            private String translation;
        }

        // Prefer explicit englishTranslation field; if absent, try to extract from translations array
        public String getEnglishTranslation() {
            if (englishTranslation != null && !englishTranslation.isBlank()) return englishTranslation;
            if (translations != null && !translations.isEmpty()) {
                for (Translation t : translations) {
                    if (t == null) continue;
                    String type = t.getTranslationType();
                    if (type != null && type.toLowerCase().contains("english")) {
                        return t.getTranslation();
                    }
                }
                // fallback to first translation entry
                Translation first = translations.get(0);
                if (first != null) return first.getTranslation();
            }
            return englishTranslation;
        }
    }
}
