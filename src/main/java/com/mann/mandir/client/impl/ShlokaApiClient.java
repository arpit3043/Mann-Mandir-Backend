package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.mann.mandir.client.BaseApiClient;
import com.mann.mandir.config.ApiProperties;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Optional;

@Slf4j
@Component
public class ShlokaApiClient extends BaseApiClient {

    private final ApiProperties apiProps;

    ShlokaApiClient(WebClient.Builder builder, ApiProperties apiProps,
                    @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                    @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getShloka().getBaseUrl();
    }

    public Optional<ShlokaResponse> getRandomShloka() {
        return get("/sanskrit/slogan/random", ShlokaResponse.class);
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ShlokaResponse {
        private String id;
        private String text;
        private String meaning;
        private String source;
        private String deity;
    }
}
