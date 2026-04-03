package com.mann.mandir.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.time.Instant;
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Builder
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    private ErrorDetail errorDetail;
    private PaginationMeta paginationMeta;

    @Builder.Default
    private Instant timestamp = Instant.now();

    public static <T> ApiResponse<T> ok(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .build();
    }

    public static <T> ApiResponse<T> ok(T data, String message) {
        return ApiResponse.<T>builder()
                .success(true)
                .message(message)
                .data(data)
                .build();
    }

    public static <T> ApiResponse<T> ok(T data, PaginationMeta pagination) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .paginationMeta(pagination)
                .build();
    }

    public static <T> ApiResponse<T> error(String code, String message) {
        return ApiResponse.<T>builder()
                .success(false)
                .errorDetail(
                        ErrorDetail.builder()
                                .code(code)
                                .message(message)
                                .build()
                )
                .build();
    }

    @Data
    @Builder
    public static class ErrorDetail {
        private String code;
        private String message;
    }

    @Data
    @Builder
    public static class PaginationMeta {
        private int page;
        private int size;
        private long totalElements;
        private long totalPages;
        private boolean hasNext;
        private boolean hasPrevious;

        public static PaginationMeta of(int page, int size, long total) {
            int totalPages = (int) Math.ceil((double) total / size);
            return PaginationMeta.builder()
                    .page(page)
                    .size(size)
                    .totalElements(total)
                    .totalPages(totalPages)
                    .hasNext(page < totalPages - 1)
                    .hasPrevious(page > 0)
                    .build();
        }
    }
}
