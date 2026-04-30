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
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

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
        return getWrappedMantras("/mantras?limit=" + limit);
    }

    public Optional<List<MantraResponse>> getMantras(String name, int limit) {
        return getWrappedMantras("/mantras?name=" + name + "&limit=" + limit);
    }

    private Optional<List<MantraResponse>> getWrappedMantras(String path) {
        Optional<Map<String, Object>> response = get(path, new ParameterizedTypeReference<>() {
        });

        if (response.isEmpty()) {
            return Optional.empty();
        }

        Object raw = response.get().get("mantras");
        if (!(raw instanceof List<?> rawList)) {
            return Optional.empty();
        }

        List<MantraResponse> items = rawList.stream()
                .filter(Map.class::isInstance)
                .map(Map.class::cast)
                .map(this::toMantraResponse)
                .collect(Collectors.toList());

        return Optional.of(items);
    }

    private MantraResponse toMantraResponse(Map<?, ?> raw) {
        MantraResponse item = new MantraResponse();
        item.setId(stringOf(raw.get("_id")));
        item.setName(stringOf(raw.get("name")));
        item.setText(stringOf(raw.get("shloka")));
        item.setMeaning(stringOf(raw.get("purpose")));
        item.setDeity(stringOf(raw.get("godName")));
        item.setTags(List.of());
        return item;
    }

    private String stringOf(Object value) {
        return value == null ? "" : value.toString();
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
