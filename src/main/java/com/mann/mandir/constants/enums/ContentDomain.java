package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum ContentDomain {

    GOD("god", "Devotional content"),
    SCRIPTURES("scriptures", "Hindu scriptures"),
    VEDAS("vedas", "Vedic literature"),
    SEARCH("search", "Cross-domain search");

    private final String path;
    private final String description;

    public static ContentDomain fromString(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        for (ContentDomain domain : values()) {
            if (domain.path.equalsIgnoreCase(value) || domain.name().equalsIgnoreCase(value)) {
                return domain;
            }
        }
        throw new IllegalArgumentException("Unknown domain: " + value);
    }
}
