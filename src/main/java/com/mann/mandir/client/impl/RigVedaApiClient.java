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
public class RigVedaApiClient extends BaseApiClient {

    private final ApiProperties apiProps;

    RigVedaApiClient(WebClient.Builder builder, ApiProperties apiProps,
                     @Value("${webclient.retry.max-attempts:3}") int maxRetries,
                     @Value("${webclient.retry.backoff-ms:500}") long retryBackoffMs) {
        super(builder, maxRetries, retryBackoffMs);
        this.apiProps = apiProps;
    }

    @Override
    protected String getBaseUrl() {
        return apiProps.getRigveda().getBaseUrl();
    }

    public Optional<List<RigVedaVerseResponse>> getByMandala(int mandala) {
        return get("/meta/book/" + mandala, new ParameterizedTypeReference<>() {
        });
    }

    public Optional<List<RigVedaVerseResponse>> getByDeity(String deity) {
        return get("/meta/god/" + deity, new ParameterizedTypeReference<>() {
        });
    }

    public Optional<List<RigVedaVerseResponse>> getByPoet(String poet) {
        return get("/meta/poet/" + poet, new ParameterizedTypeReference<>() {
        });
    }

    public Optional<List<RigVedaVerseResponse>> getByMeter(String meter) {
        return get("/meta/meter/" + meter, new ParameterizedTypeReference<>() {
        });
    }

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class RigVedaVerseResponse {
        private int mandal;
        private int sukta;
        private int stanza;
        private String sungby;
        private String sungbycategory;
        private String sungfor;
        private String sungforcategory;
        private String meter;
    }
}
