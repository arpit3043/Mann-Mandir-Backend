package com.mann.mandir.client.impl;

import com.mann.mandir.client.BaseApiClient;
import com.mann.mandir.config.ApiProperties;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;
import java.util.Optional;

@Slf4j
@Component
public class DharmicDataClient extends BaseApiClient {

    private final ApiProperties apiProperties;

    DharmicDataClient(WebClient.Builder builder, ApiProperties apiProperties,
                      @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                      @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProperties = apiProperties;
    }

    @Override
    protected String getBaseUrl() {
        return apiProperties.getDharmicdata().getBaseUrl();
    }

    public Optional<Map<String, Object>> getMahabharataParva(int parvaNumber) {
        return get("/mahabharata/parva-" + parvaNumber + ".json", new ParameterizedTypeReference<>() {
        });
    }

    public Optional<Map<String, Object>> getRamayanaKanda(String kanda) {
        return get("/ramayana/" + kanda + ".json", new ParameterizedTypeReference<>() {
        });
    }

    public Optional<Map<String, Object>> getYajurVeda() {
        return get("/yajurveda/yajurveda.json", new ParameterizedTypeReference<>() {
        });
    }

    public Optional<Map<String, Object>> getAtharvaVeda() {
        return get("/atharvaveda/atharvaveda.json", new ParameterizedTypeReference<>() {
        });
    }
}
