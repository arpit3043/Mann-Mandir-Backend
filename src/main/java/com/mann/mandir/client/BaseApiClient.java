package com.mann.mandir.client;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.Optional;

@Slf4j
@RequiredArgsConstructor
public abstract class BaseApiClient {

    private final WebClient.Builder webClientBuilder;
    private final int maxRetries;
    private final long retryBackoffMs;

    protected abstract String getBaseUrl();

    protected WebClient client() {
        return webClientBuilder.baseUrl(getBaseUrl()).build();
    }

    protected <T> Optional<T> get(String path, Class<T> type) {
        try {
            T result = client()
                    .get()
                    .uri(path)
                    .retrieve()
                    .bodyToMono(type)
                    .retryWhen(retrySpec())
                    .block();
            return Optional.ofNullable(result);
        } catch (WebClientResponseException webClientResponseException) {
            log.warn("HTTP {} for {}{}: {}", webClientResponseException.getStatusCode(),
                    getBaseUrl(), path, webClientResponseException.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Error calling {}{}: {}", getBaseUrl(), path, e.getMessage());
            return Optional.empty();
        }
    }

    protected <T> Optional<T> get(String path, ParameterizedTypeReference<T> type) {
        try {
            T result  = client()
                    .get()
                    .uri(path)
                    .retrieve()
                    .bodyToMono(type)
                    .retryWhen(retrySpec())
                    .block();
            return Optional.ofNullable(result);
        } catch (WebClientResponseException webClientResponseException) {
            log.warn("HTTP {} for {}{}: {}", webClientResponseException.getStatusCode(), getBaseUrl(), path, webClientResponseException.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            log.error("Error calling {}{}: {}", getBaseUrl(), path, e.getMessage());
            return Optional.empty();
        }
    }

    protected <T> Optional<T> getWithParams(String pathTemplate, Class<T>type, Object... params) {
        String path = String.format(pathTemplate, params);
        return get(path, type);
    }

    @org.jetbrains.annotations.Contract(" -> new")
    private @NotNull Retry retrySpec() {
        return Retry.backoff(maxRetries,
                Duration.ofMillis(retryBackoffMs))
                .filter(exception -> !(exception instanceof WebClientResponseException.NotFound))
                .onRetryExhaustedThrow((spec, sig) -> sig.failure());
    }
}
