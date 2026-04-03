package com.mann.mandir.client.impl;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
public class HavyakaApiClient extends BaseApiClient {

    private final ApiProperties apiProps;

    HavyakaApiClient(WebClient.Builder builder, ApiProperties apiProps,
                     @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                     @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getHavyaka().getBaseUrl();
    }

    public Optional<List<MantraResponse>> getMantras(int limit) {
        return get("/mantras?limit=" + limit, new ParameterizedTypeReference<>() {
        });
    }

    public Optional<List<MantraResponse>> getMantras(String name, int limit) {
        return get("/mantras?name=" + name + "&limit=" + limit, new ParameterizedTypeReference<>() {
        });
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MantraResponse {
        private String id;
        private String name;
        private String text;
        private String meaning;
        private String deity;
        private List<String> tags;
    }
}
