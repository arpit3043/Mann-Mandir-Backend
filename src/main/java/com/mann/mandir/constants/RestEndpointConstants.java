package com.mann.mandir.constants;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public final class RestEndpointConstants {

    public static final String BASE_URL = "/api/v1";

    // God domain
    public static final String GOD = "/god";
    public static final String AARTIS = "/aartis";
    public static final String AARTIS_BY_DEITIES = "/aartis/deities";
    public static final String STOTRAMS = "/stotram";
    public static final String MANTRAS = "/mantras";

    // Scriptures
    public static final String SCRIPTURES = "/scriptures";

    // Vedas
    public static final String VEDAS = "/vedas";
    public static final String UPANISHADS = "/upanishads";

    // Search
    public static final String SEARCH = "/search";
}
