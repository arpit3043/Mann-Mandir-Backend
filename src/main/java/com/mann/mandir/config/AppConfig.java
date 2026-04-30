package com.mann.mandir.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import com.mann.mandir.constants.CacheNames;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.CacheManager;
import org.springframework.cache.caffeine.CaffeineCache;
import org.springframework.cache.support.SimpleCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Slf4j
@Configuration
public class AppConfig {

    @Value("${webclient.timeout.connect:5000}")
    private int connectTimeoutMs;

    @Value("${webclient.timeout.read:10000}")
    private int readTimeoutMs;

    @Value("${webclient.timeout.write:5000}")
    private int writeTimeoutMs;

    @Value("${cache.gita.spec:5000}")
    private String gitaSpec;

    @Value("${cache.veda.spec:5000}")
    private String vedaSpec;

    @Value("${cache.ramayana.spec:5000}")
    private String ramayanaSpec;

    @Value("${cache.mahabharata.spec:5000}")
    private String mahabharataSpec;

    @Value("${cache.aarti.spec:5000}")
    private String aartiSpec;

    @Value("${cache.chalisa.spec:5000}")
    private String chalisaSpec;

    @Value("${cache.stotram.spec:5000}")
    private String stotramSpec;

    @Value("${cache.mantra.spec:5000}")
    private String mantraSpec;

    @Bean
    public WebClient.Builder webClientBuilder() {
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeoutMs)
                .responseTimeout(Duration.ofMillis(readTimeoutMs))
                .doOnConnected(conn -> conn
                        .addHandlerLast(new ReadTimeoutHandler(readTimeoutMs, TimeUnit.MILLISECONDS))
                        .addHandlerLast(new WriteTimeoutHandler(writeTimeoutMs, TimeUnit.MILLISECONDS)));

        return WebClient.builder()
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                .filter(logRequest())
                .filter(logResponse());
    }

    private ExchangeFilterFunction logRequest() {
        return ExchangeFilterFunction.ofRequestProcessor(req -> {
            log.debug(">> {} {}", req.method(), req.url());
            return Mono.just(req);
        });
    }

    private ExchangeFilterFunction logResponse() {
        return ExchangeFilterFunction.ofResponseProcessor(res -> {
            log.debug("<< HTTP {}", res.statusCode());
            return Mono.just(res);
        });
    }

    @Bean
    public CacheManager cacheManager() {
        List<CaffeineCache> caches = Arrays.asList(
                buildCache(CacheNames.GITA, gitaSpec),
                buildCache(CacheNames.VEDA, vedaSpec),
                buildCache(CacheNames.RAMAYANA, ramayanaSpec),
                buildCache(CacheNames.MAHABHARATA, mahabharataSpec),
                buildCache(CacheNames.AARTI, aartiSpec),
                buildCache(CacheNames.CHALISA, chalisaSpec),
                buildCache(CacheNames.STOTRAM, stotramSpec),
                buildCache(CacheNames.MANTRA, mantraSpec)
        );
        SimpleCacheManager manager = new SimpleCacheManager();
        manager.setCaches(caches);
        return manager;
    }

    private CaffeineCache buildCache(String name, String spec) {
        return new CaffeineCache(name, Caffeine.from(spec).build());
    }
}
