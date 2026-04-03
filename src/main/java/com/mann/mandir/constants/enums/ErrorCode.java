package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {

    NOT_FOUND("NOT_FOUND", "The requested resource was not found"),
    VALIDATION_ERROR("VALIDATION_ERROR", "Request validation failed"),
    BAD_REQUEST("BAD_REQUEST", "The request was invalid"),
    INTERNAL_ERROR("INTERNAL_ERROR", "An unexpected error occurred"),
    EXTERNAL_API_ERROR("EXTERNAL_API_ERROR", "External API call failed"),
    RATE_LIMITED("RATE_LIMITED", "Too many requests");

    private final String code;
    private final String defaultMessage;
}
