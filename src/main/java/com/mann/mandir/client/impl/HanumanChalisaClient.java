package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.mann.mandir.client.BaseApiClient;
import com.mann.mandir.config.ApiProperties;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Optional;

@Slf4j
@Component
public class HanumanChalisaClient extends BaseApiClient {

    private final ApiProperties apiProps;

    HanumanChalisaClient(WebClient.Builder builder, ApiProperties apiProps,
                         @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                         @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getChalisa().getHanuman().getBaseUrl();
    }

    public Optional<List<ChalisaVerseResponse>> getAllVerses() {
        return get("/verses", new ParameterizedTypeReference<>() {
        });
    }

    public Optional<ChalisaVerseResponse> getVerse(int number) {
        return get("/verses/" + number, ChalisaVerseResponse.class);
    }

    public Optional<ChalisaVerseResponse> getRandomVerse() {
        return get("/random", ChalisaVerseResponse.class);
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ChalisaVerseResponse {
        private int number;
        private String type;
        private String devanagari;
        private String transliteration;
        @JsonProperty("english_translation")
        private String englishTranslation;
        @JsonProperty("hindi_translation")
        private String hindiTranslation;
        private String meter;
        private List<String> tags;
        private String summary;
    }
}
